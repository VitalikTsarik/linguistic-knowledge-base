import nltk

from dictionary.helpers import processRawTexts


def getTagsStat(filenames):
    tagsdict = nltk.data.load('help/tagsets/upenn_tagset.pickle')
    tags = {}
    for key in tagsdict.keys():
        tags[key] = 0

    for filename in filenames:
        with open(filename, encoding='utf-8') as file:
            text = file.read()
            for tag in tags:
                tags[tag] += text.count(tag)

    return tags


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
