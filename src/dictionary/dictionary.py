from os import listdir
from os.path import basename, join
from shutil import copyfile
from tempfile import TemporaryDirectory

import nltk
from editor import editor

from dictionary.constants import Keys
from dictionary.helpers import saveToFile, openDictionary, readAndTagTexts, mergeDicts, tagWord, \
    readTexts, getBaseForm

TAGGED_POSTFIX = '.tagged'
AVAILABLE_TAGS = set(nltk.load('help/tagsets/upenn_tagset.pickle'))


class Dictionary:
    def __init__(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__tempDir = TemporaryDirectory()

    def addTexts(self, filenames):
        for filename in filenames:
            tempFilename = join(self.__tempDir.name, basename(filename))
            copyfile(filename, tempFilename)

        textsData, taggedTexts = readAndTagTexts(filenames)
        for filename, text in taggedTexts.items():
            tempFilename = self.getTaggedFilename(join(self.__tempDir.name, basename(filename)))
            with open(tempFilename, 'w') as file:
                file.write(text)

        self.__dictionary = mergeDicts(self.__dictionary, textsData)

    def editText(self, filename):
        editor(filename=join(self.__tempDir.name, filename))
        filenames = self.textsTempFilenames
        self.__dictionary, _ = readTexts(filenames)

    def editTaggedText(self, filename):
        editor(filename=join(self.__tempDir.name, filename))

    def addWord(self, word):
        if word in self.__dictionary:
            return False

        tag = tagWord(word)
        self.__dictionary[word] = {
            Keys.occurrence.value: 0,
            Keys.tags.value: {tag},
            Keys.base.value: {getBaseForm(word, tag)},
        }
        return True

    def removeWords(self, words):
        for word in words:
            self.__dictionary.pop(word)

    @property
    def tableRecords(self):
        return [[
            key,
            value[Keys.occurrence.value],
            ', '.join(value[Keys.tags.value]),
            ', '.join(value[Keys.base.value]),
        ] for key, value in self.__dictionary.items()]

    def save(self, filename=None):
        if filename:
            self.__currentFilename = filename

        texts = []
        for textName in self.textsNames:
            filePath = self.getTempTextPath(textName)
            texts.append({
                'name': textName,
                'content': open(filePath, 'r').read(),
                'tagged': open(self.getTaggedFilename(filePath), 'r').read()
            })
        data = {
            'data': self.__dictionary,
            'texts': texts,
        }
        saveToFile(self.__currentFilename, data)

    def open(self, filename):
        if self.__tempDir:
            self.__tempDir.cleanup()

        self.__tempDir = TemporaryDirectory()
        self.__dictionary, texts = openDictionary(filename)
        for textData in texts:
            tempFilePath = join(self.__tempDir.name, textData['name'])
            with open(tempFilePath, 'w', encoding='utf-8') as file:
                file.write(textData['content'])
            with open(self.getTaggedFilename(tempFilePath), 'w', encoding='utf-8') as file:
                file.write(textData['tagged'])

        self.__currentFilename = filename

    def clear(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__tempDir.cleanup()

    def editWord(self, oldWord, newWord):
        if not newWord:
            return

        newWordData = self.__dictionary.get(newWord)
        if newWordData is None:
            newWordData = {
                Keys.occurrence.value: 0,
                Keys.tags.value: {tagWord(newWord)},
            }
        newWordData[Keys.occurrence.value] += self.__dictionary[oldWord][Keys.occurrence.value]
        self.__dictionary[newWord] = newWordData
        self.__dictionary.pop(oldWord)

    def editTags(self, word, newTags):
        tags = set(newTags.replace(' ', '').split(','))
        if all(tag in AVAILABLE_TAGS for tag in tags):
            self.__dictionary[word][Keys.tags.value] = tags

    def editBase(self, word, newBases):
        bases = set(newBases.replace(' ', '').split(','))
        self.__dictionary[word][Keys.base.value] = bases

    @property
    def textsNames(self):
        return [name for name in listdir(self.__tempDir.name) if not name.endswith(TAGGED_POSTFIX)]

    @property
    def taggedTextsNames(self):
        return [name for name in listdir(self.__tempDir.name) if name.endswith(TAGGED_POSTFIX)]

    @staticmethod
    def getTaggedFilename(filename):
        return filename + TAGGED_POSTFIX

    def getTempTextPath(self, textName):
        return join(self.__tempDir.name, textName)

    @property
    def textsTempFilenames(self):
        return [self.getTempTextPath(textName) for textName in self.textsNames]

    @property
    def taggedTextsTempFilenames(self):
        return [self.getTempTextPath(textName) for textName in self.taggedTextsNames]
