import json
import re

from dictionary.constants import Keys


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


def readTexts(filenames):
    words = processRawTexts(filenames)
    data = {}
    for word in words:
        if word in data.keys():
            data[word][Keys.occurrence.value] += 1
        else:
            data[word] = {Keys.occurrence.value: 1}

    return data


def mergeDicts(a, b):
    result = a.copy()
    for key, value in b.items():
        if key in result.keys():
            result[key][Keys.occurrence.value] += value[Keys.occurrence.value]
        else:
            result[key] = {Keys.occurrence.value: value[Keys.occurrence.value]}
    return result


def saveDictionary(filename, dictionary):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file)


def openDictionary(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        dictionary = json.load(file)
        return dictionary
