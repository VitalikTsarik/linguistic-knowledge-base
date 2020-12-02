import pickle
import re
from fileinput import FileInput

import nltk
from nltk import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.tag import pos_tag

from dictionary.constants import Keys

PUNCTUATION_TAGS = [
    ('.', '.'),
    ('!', '.'),
    ('?', '.'),
    ('...', '.'),
    (',', ','),
    ('(', '('),
    ('[', '('),
    ('{', '('),
    (')', ')'),
    (']', ')'),
    ('}', ')'),
    ('\"', '\"'),
    ('\'', '\"'),
    ('\'\'', '\"'),
    (':', ':'),
    (';', ':'),
    ('-', '-'),
]

PUNCTUATION = [val for val, _ in PUNCTUATION_TAGS]


def processRawTexts(filenames):
    words = []
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as processed_file:
            text = processed_file.read()
            text = text.replace('\n', ' ')
            text = re.sub('[^A-Za-z \'.]', '', text)
            tokens = word_tokenize(text)
            for token in tokens:
                if token in PUNCTUATION:
                    tokens.remove(token)
            words.extend(tokens)
    return words


def processWords(words):
    taggedWords = nltk.pos_tag(words)

    data = {}
    for word, tag in taggedWords:
        if word in data.keys():
            data[word][Keys.occurrence.value] += 1
            data[word][Keys.tags.value].add(tag)
            data[word][Keys.base.value].add(getBaseForm(word, tag))
        else:
            data[word] = {
                Keys.occurrence.value: 1,
                Keys.tags.value: {tag},
                Keys.base.value: {getBaseForm(word, tag)},
            }
    return data, taggedWords


def readTexts(filenames):
    words = processRawTexts(filenames)
    data, taggedWords = processWords(words)
    return data, taggedWords


def readAndTagTexts(filenames):
    data, taggedWords = readTexts(filenames)
    taggedWords.extend(PUNCTUATION_TAGS)
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
                Keys.base.value: value[Keys.base.value],
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
    tokens = pos_tag([word])
    _, tag = tokens[0]
    return tag


def getWordnetPos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def getTagFromPos(pos):
    if pos == wordnet.ADJ:
        return 'JJ'
    elif pos == wordnet.VERB:
        return 'VB'
    elif pos == wordnet.ADV:
        return 'RB'
    return 'NN'


lemmatizer = WordNetLemmatizer()


def getBaseForm(word, tag):
    pos = getWordnetPos(tag)
    base = lemmatizer.lemmatize(word, pos)
    return f'{base}_{tag}'


def replaceWord(oldWord, newWord, filenames):
    for filename in filenames:
        with FileInput(filename, inplace=True) as file:
            for line in file:
                line.replace(rf'\b{oldWord}\b', newWord)


def removeWord(word, filenames):
    replaceWord(word, '', filenames)
