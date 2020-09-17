import os

from constants import PROCESSED_DIR_PATH


def read_processed_texts():
    data = {}
    for filename in os.listdir(PROCESSED_DIR_PATH):
        with open(os.path.join(PROCESSED_DIR_PATH, filename), 'r') as file:
            for line in file:
                word = line.strip('\n')
                data[word] = data.setdefault(word, 0) + 1

    return data
