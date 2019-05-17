

from models import GreedySearchDecoder, chat
from settings import TRAIN_BEFORE_CHAT
from train import init, trainWrapper

print("Initialising...")
(encoder, decoder,
 encoder_optimizer, decoder_optimizer,
 embedding, voc, pairs_of_sentences, checkpoint) = init()
print("Done")
print("Starting Training!")
if TRAIN_BEFORE_CHAT:
    trainWrapper(voc, pairs_of_sentences, encoder, decoder,
                 encoder_optimizer, decoder_optimizer,
                 embedding, checkpoint)
# Tchat  !
encoder.eval()
decoder.eval()
# Initialize search module
searcher = GreedySearchDecoder(encoder, decoder)
chat(encoder, decoder, searcher, voc)
