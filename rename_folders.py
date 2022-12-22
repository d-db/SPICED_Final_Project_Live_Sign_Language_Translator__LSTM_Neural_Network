"""
Script to adjust folder names within a specific folder.
Can be used when adding more recorded iterations of one sign to the folder.
The creator of this project, for example, started with 30 recordings of a specific sign.
Over time, when the amount of vocabularies grew, the number of recordings where increased to
150, 300, 500 and eventually 700 for the model to work robust enough.
This made it necessary to rename a hugh amount of folders.
"""

import os

# How many folders do you want to rename?
NO_SEQUENCES = 200
# Which name should carry the first renamed folder?
START_VALUE = 500
DATA_PATH = "./data/{add_the_folder_name}/"

# Listing directories
print("The dir is: %s"%os.listdir(os.getcwd()))

for sequence in range(NO_SEQUENCES):
    path_1 = DATA_PATH + str(sequence)
    path_2 = DATA_PATH + str(START_VALUE)
    os.rename(path_1, path_2)
    START_VALUE \
        += 1