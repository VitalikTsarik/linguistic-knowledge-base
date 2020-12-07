import nltk


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
