from os import listdir
from os.path import basename, join
from shutil import copyfile
from tempfile import TemporaryDirectory

from editor import editor

from dictionary.constants import Keys
from dictionary.helpers import saveToFile, openDictionary, readAndTagTexts, mergeDicts, readTextsFromDir, tagWord

TAGGED_POSTFIX = '.tagged'


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
            tempFilename = self.__getTaggedFilename(join(self.__tempDir.name, basename(filename)))
            with open(tempFilename, 'w') as file:
                file.write(text)

        self.__dictionary = mergeDicts(self.__dictionary, textsData)

    def editText(self, filename):
        editor(filename=join(self.__tempDir.name, filename))
        self.__dictionary = readTextsFromDir(self.__tempDir.name)

    @property
    def textsNames(self):
        return [name for name in listdir(self.__tempDir.name) if not name.endswith(TAGGED_POSTFIX)]

    def addWord(self, word):
        if word in self.__dictionary:
            return False

        self.__dictionary[word] = {
            Keys.occurrence.value: 0,
            Keys.tag.value: tagWord(word),
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
            value[Keys.tag.value],
        ] for key, value in self.__dictionary.items()]

    def save(self, filename=None):
        if filename:
            self.__currentFilename = filename

        texts = []
        for textName in self.textsNames:
            filePath = join(self.__tempDir.name, textName)
            texts.append({
                'name': textName,
                'content': open(filePath, 'r').read(),
                'tagged': open(self.__getTaggedFilename(filePath), 'r').read()
            })
        data = {
            'data': self.__dictionary,
            'texts': texts,
        }
        saveToFile(self.__currentFilename, data)

    def open(self, filename):
        self.__tempDir = TemporaryDirectory()
        self.__dictionary, texts = openDictionary(filename)
        for textData in texts:
            tempFilePath = join(self.__tempDir.name, textData['name'])
            with open(tempFilePath, 'w', encoding='utf-8') as file:
                file.write(textData['content'])
            with open(self.__getTaggedFilename(tempFilePath), 'w', encoding='utf-8') as file:
                file.write(textData['tagged'])

        self.__currentFilename = filename

    def clear(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__tempDir.cleanup()

    def editWord(self, oldWord, newWord):
        newWordData = self.__dictionary.get(newWord)
        if newWordData is None:
            newWordData = {
                Keys.occurrence.value: 0,
                Keys.tag.value: tagWord(newWord),
            }
        newWordData[Keys.occurrence.value] += self.__dictionary[oldWord][Keys.occurrence.value]
        self.__dictionary[newWord] = newWordData
        self.__dictionary.pop(oldWord)

    @staticmethod
    def __getTaggedFilename(filename):
        return filename + TAGGED_POSTFIX
