import os
import re

import torch

# ########
# TOKENS #
# ########
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token
NWL_token = 3  # New line token

# #############################
# Regex to apply on sentences #
# #############################
SUBSTITUTES = [re.compile(r"(\w+)(\.+$)"),     # hello... => hello ...
               re.compile(r"(\w+)(\^+$)"),     # hello^^ => hello ^^
               re.compile(r"(\w+)(\?+$)"),     # hello??? => hello ???
               re.compile(r"(^\()(\w+)"),      # (hello => ( hello
               re.compile(r"(\w+)(!+$)"),      # hello!!! => hello !!!
               re.compile(r"(\w+)((?<!:)\))")  # hello) => hello ) but :) pass
               ]

# ##################
# Names for saving #
# ##################
SAVE_DIR = './saves'
MODEL_NAME = 'ChatBotFacebookPierre'

# #####################
# Training parameters #
# #####################
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLIP = 50.0
LEARNING_RATE = 0.0001
N_ITERATION = 1000
BATCH_SIZE = 128
TEACHER_FORCING_RATIO = 0.8
DECODER_LEARNING_RATIO = 5.0

# #########################
# Architecture parameters #
# #########################
ATTN_MODEL = 'dot'  # 'general' 'concat'
HIDDEN_SIZE = 500
ENCODER_N_LAYERS = 2
DECODER_N_LAYERS = 2
DROPOUT = 0.1

# ################################
# Checkpoint and Save parameters #
# ################################
# Restart and finish training ? Or start again from scratch
# Please give the iter number if you want to restart

# Do you want to load a saved model ?
RESTART = False
load_checkpoint = False           # <== Load previous state ??
if load_checkpoint:
    iter_to_restart = 350      # <== Give the iter to restart
    if iter_to_restart != 0:
        RESTART = True
    LOADFILENAME = os.path.join(SAVE_DIR, MODEL_NAME,
                                f'{ENCODER_N_LAYERS}-{DECODER_N_LAYERS}_{HIDDEN_SIZE}',
                                f'{iter_to_restart}_checkpoint.tar')
else:
    LOADFILENAME = None
PRINT_EVERY = 1
SAVE_EVERY = 50

# #################
# Chat parameters #
# #################
TRAIN_BEFORE_CHAT = True
MAX_LENGTH = 100
