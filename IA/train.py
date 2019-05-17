
import os
import random

import torch
import torch.nn as nn
from torch import optim

from cleanAndPrepare import (get_chat_friend_and_me, get_discussions,
                             load_all_json_conv, make_pairs)
from models import EncoderRNN, LuongAttnDecoderRNN, maskNLLLoss
from preparePytorch import batch2TrainData
from settings import (ATTN_MODEL, BATCH_SIZE, CLIP, DECODER_LEARNING_RATIO,
                      DECODER_N_LAYERS, DEVICE, DROPOUT, ENCODER_N_LAYERS,
                      HIDDEN_SIZE, LEARNING_RATE, LOADFILENAME, MODEL_NAME,
                      N_ITERATION, PRINT_EVERY, RESTART, SAVE_DIR, SAVE_EVERY,
                      TEACHER_FORCING_RATIO, SOS_token)
from vocabulary import Voc


def init():
    print("\tInitialising sentences")

    print("\t\tLoading and cleaning json files")
    json_of_convs = load_all_json_conv('./Dataset/messages')

    print("\t\tLoading two person convs")
    duo_conversations = get_chat_friend_and_me(json_of_convs)

    print("\t\tMaking two person convs discussions")
    discussions = get_discussions(duo_conversations)

    print("\t\tCreating pairs for training")
    pairs_of_sentences = make_pairs(discussions)
    print(f"\t\t{len(pairs_of_sentences)} different pairs")

    print("\t\tCreating Vocabulary")
    voc = Voc()

    print("\t\tPopulating Vocabulary")
    voc.createVocFromPairs(pairs_of_sentences)
    print(f"\t\tVocabulary of : {voc.num_words} differents words")

    print('\tBuilding encoder and decoder ...')
    embedding = nn.Embedding(voc.num_words, HIDDEN_SIZE)
    encoder = EncoderRNN(HIDDEN_SIZE, embedding, ENCODER_N_LAYERS, DROPOUT)
    decoder = LuongAttnDecoderRNN(ATTN_MODEL, embedding, HIDDEN_SIZE,
                                  voc.num_words, DECODER_N_LAYERS, DROPOUT)
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=LEARNING_RATE)
    decoder_optimizer = optim.Adam(decoder.parameters(),
                                   lr=LEARNING_RATE * DECODER_LEARNING_RATIO)
    checkpoint = None
    if LOADFILENAME:
        print("\t\tLoading last training")
        checkpoint = torch.load(LOADFILENAME)
        # If loading a model trained on GPU to CPU
        # checkpoint=torch.load(loadFilename,map_location=torch.device('cpu'))
        encoder_sd = checkpoint['en']
        decoder_sd = checkpoint['de']
        encoder_optimizer_sd = checkpoint['en_opt']
        decoder_optimizer_sd = checkpoint['de_opt']
        embedding_sd = checkpoint['embedding']
        voc.__dict__ = checkpoint['voc_dict']
        print("\t\tPopulating from last training")
        embedding.load_state_dict(embedding_sd)
        encoder.load_state_dict(encoder_sd)
        decoder.load_state_dict(decoder_sd)
        encoder_optimizer.load_state_dict(encoder_optimizer_sd)
        decoder_optimizer.load_state_dict(decoder_optimizer_sd)

    encoder = encoder.to(DEVICE)
    decoder = decoder.to(DEVICE)
    return (encoder, decoder,
            encoder_optimizer, decoder_optimizer,
            embedding, voc, pairs_of_sentences, checkpoint)


def train(input_variable, lengths, target_variable, mask, max_target_len,
          encoder, decoder, embedding, encoder_optimizer, decoder_optimizer):

    # Zero gradients
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    # Set device options
    input_variable = input_variable.to(DEVICE)
    lengths = lengths.to(DEVICE)
    target_variable = target_variable.to(DEVICE)
    mask = mask.to(DEVICE)

    # Initialize variables
    loss = 0
    print_losses = []
    n_totals = 0

    # Forward pass through encoder
    encoder_outputs, encoder_hidden = encoder(input_variable, lengths)

    # Create initial decoder input (start with SOS tokens for each sentence)
    decoder_input = torch.LongTensor([[SOS_token for _ in range(BATCH_SIZE)]])
    decoder_input = decoder_input.to(DEVICE)

    # Set initial decoder hidden state to the encoder's final hidden state
    decoder_hidden = encoder_hidden[:decoder.n_layers]

    # Determine if we are using teacher forcing this iteration
    use_teacher_forcing = (True if random.random() < TEACHER_FORCING_RATIO
                           else False)

    # Forward batch of sequences through decoder one time step at a time
    if use_teacher_forcing:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # Teacher forcing: next input is current target
            decoder_input = target_variable[t].view(1, -1)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, target_variable[t],
                                            mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal
    else:
        for t in range(max_target_len):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # No teacher forcing: next input is decoder's own current output
            _, topi = decoder_output.topk(1)
            decoder_input = torch.LongTensor([[topi[i][0]
                                               for i in range(BATCH_SIZE)]])
            decoder_input = decoder_input.to(DEVICE)
            # Calculate and accumulate loss
            mask_loss, nTotal = maskNLLLoss(decoder_output,
                                            target_variable[t],
                                            mask[t])
            loss += mask_loss
            mask_loss.detach_()
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal

    # Perform backpropatation
    loss.backward()

    # Detach to avoid memory leaks
    decoder_hidden.detach_()
    encoder_hidden.detach_()
    decoder_input = decoder_input.detach()
    decoder_output.detach_()
    encoder_outputs.detach_()

    # Clip gradients: gradients are modified in place
    _ = nn.utils.clip_grad_norm_(encoder.parameters(), CLIP)
    _ = nn.utils.clip_grad_norm_(decoder.parameters(), CLIP)

    # Adjust model weights
    encoder_optimizer.step()
    decoder_optimizer.step()

    return sum(print_losses) / n_totals


def trainWrapper(voc, pairs, encoder, decoder, encoder_optimizer,
                 decoder_optimizer, embedding, checkpoint):

    # Load batches for each iteration
    training_batches = [batch2TrainData(voc, [random.choice(pairs)
                                              for _ in range(BATCH_SIZE)])
                        for _ in range(N_ITERATION)]

    start_iteration = 1
    print_loss = 0
    if LOADFILENAME and RESTART:
        start_iteration = checkpoint['iteration'] + 1

    # Training loop
    print("Training...")
    for iteration in range(start_iteration, N_ITERATION + 1):
        training_batch = training_batches[iteration - 1]
        # Extract fields from batch
        (input_variable, lengths,
         target_variable, mask, max_target_len) = training_batch

        # Run a training iteration with batch
        loss = train(input_variable, lengths,
                     target_variable, mask, max_target_len,
                     encoder, decoder, embedding,
                     encoder_optimizer, decoder_optimizer)
        print_loss += loss

        # Print progress
        if iteration % PRINT_EVERY == 0:
            print_loss_avg = print_loss / PRINT_EVERY
            print(f"Iteration: {iteration};  ",
                  f"Percent complete: {(iteration / N_ITERATION * 100):.1f}% ",
                  f"Average loss: {print_loss_avg:.4f}")
            print_loss = 0

        # Save checkpoint
        if (iteration % SAVE_EVERY == 0):
            directory = os.path.join(SAVE_DIR, MODEL_NAME,
                                     '{}-{}_{}'.format(ENCODER_N_LAYERS,
                                                       DECODER_N_LAYERS,
                                                       HIDDEN_SIZE))
            if not os.path.exists(directory):
                os.makedirs(directory)
            torch.save({
                'iteration': iteration,
                'en': encoder.state_dict(),
                'de': decoder.state_dict(),
                'en_opt': encoder_optimizer.state_dict(),
                'de_opt': decoder_optimizer.state_dict(),
                'loss': loss,
                'voc_dict': voc.__dict__,
                'embedding': embedding.state_dict()
            }, os.path.join(directory, f'{iteration}_checkpoint.tar'))
