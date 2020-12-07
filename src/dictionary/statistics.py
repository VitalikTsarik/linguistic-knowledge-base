from itertools import tee, chain, islice

import nltk

from dictionary.helpers import processRawTexts, getAvailableTags


def getTagsStat(filenames):
    tags = getAvailableTags()
    data = {}
    for tag in tags:
        data[tag] = 0

    for filename in filenames:
        with open(filename, encoding='utf-8') as file:
            text = file.read()
            for tag in data:
                data[tag] += text.count(tag)

    return data


def getWordTagPairsStat(filenames):
    words = processRawTexts(filenames)
    taggedWords = nltk.pos_tag(words)

    data = {}
    for word, tag in taggedWords:
        pair = f'{word}_{tag}'
        if pair in data:
            data[pair] += 1
        else:
            data[pair] = 1

    return data


def _nextIter(iterable):
    items, nexts = tee(iterable, 2)
    nexts = islice(nexts, 1, None)
    return zip(items, nexts)


def getTagsPairsStat(filenames):
    words = processRawTexts(filenames)
    taggedWords = nltk.pos_tag(words)

    tags = getAvailableTags()
    data = {tag: {tag: 0 for tag in tags} for tag in tags}

    for taggedWord, nextTaggedWord in _nextIter(taggedWords):
        _, tag = taggedWord
        _, nextTag = nextTaggedWord
        data[tag][nextTag] += 1

    return data
