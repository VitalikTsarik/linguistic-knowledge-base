import os
import re

from constants import PROCESSED_DIR_PATH


def processRawTexts(filenames):
    result = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as processed_file:
            for line in processed_file:
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!])', line)
                for sentence in sentences:
                    sentence = sentence.strip(' .?!"\'\n')
                    sentence = sentence.replace('..', '')
                    sentence = sentence.replace('--', '')
                    if len(sentence) < 2:
                        continue
                    sentence = sentence[0].lower() + sentence[1:]
                    sentence = re.sub(r'[^A-Za-z\' .-]', '', sentence)
                    sentence = re.sub(r' +', ' ', sentence)
                    words = sentence.split(' ')
                    for word in words:
                        word = word.strip('\' -')
                        if word != '':
                            if len(word) > 1 and not re.search(r'[A-Z]+[a-z]+$', word):
                                word = word.lower()
                            result.append(word)
    return result


def read_processed_texts():
    data = {}
    for filename in os.listdir(PROCESSED_DIR_PATH):
        with open(os.path.join(PROCESSED_DIR_PATH, filename), 'r') as file:
            for line in file:
                word = line.strip('\n')
                data[word] = data.setdefault(word, 0) + 1

    return data


def readTexts(filenames):
    words = processRawTexts(filenames)
    data = {}
    for word in words:
        data[word] = data.setdefault(word, 0) + 1

    return data


def mergeDicts(a, b):
    result = a.copy()
    for key, value in b.items():
        result[key] = result.setdefault(key, 0) + value
    return result
