import pickle
import re
from fileinput import FileInput

import nltk

from dictionary.constants import Keys

PUNCTUATION = [
    ('.', '.'),
    ('!', '.'),
    ('?', '.'),
    (',', ','),
    ('(', '('),
    ('[', '('),
    ('{', '('),
    (')', ')'),
    (']', ')'),
    ('}', ')'),
    ('\"', '\"'),
    ('\'', '\"'),
    (':', ':'),
    (';', ':'),
    ('-', '-'),
]


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
    taggedWords = nltk.pos_tag(words)
    data = {}
    for word, tag in taggedWords:
        if word in data.keys():
            data[word][Keys.occurrence.value] += 1
        else:
            data[word] = {
                Keys.occurrence.value: 1,
                Keys.tags.value: {tag},
            }
    return data, taggedWords


def readAndTagTexts(filenames):
    data, taggedWords = readTexts(filenames)
    taggedWords.extend(PUNCTUATION)
    taggedTexts = tagTexts(filenames, taggedWords)
    return data, taggedTexts


def tagTexts(filenames, taggedWords):
    taggedTexts = {}
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            text = text.replace('.', ' .')
            text = text.replace(',', ' ,')
            replacements = dict((re.escape(word), f'{word}_{tag}') for word, tag in taggedWords)
            pattern = re.compile("|".join(replacements.keys()))
            text = pattern.sub(lambda m: replacements[re.escape(m.group(0))], text)
            taggedTexts[filename] = text
    return taggedTexts


def mergeDicts(a, b):
    result = a.copy()
    for key, value in b.items():
        if key in result.keys():
            result[key][Keys.occurrence.value] += value[Keys.occurrence.value]
            # TODO: merge tags set
        else:
            result[key] = {
                Keys.occurrence.value: value[Keys.occurrence.value],
                Keys.tags.value: value[Keys.tags.value],
            }
    return result


def saveToFile(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def openDictionary(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        dictionary = data['data']
        texts = data['texts']
        return dictionary, texts


def tagWord(word):
    tokens = nltk.pos_tag([word])
    _, tag = tokens[0]
    return {tag}


def replaceWord(oldWord, newWord, filenames):
    for filename in filenames:
        with FileInput(filename, inplace=True, backup='.bak') as file:
            for line in file:
                line.replace(rf'\b{oldWord}\b', newWord)


def removeWord(word, filenames):
    replaceWord(word, '', filenames)
