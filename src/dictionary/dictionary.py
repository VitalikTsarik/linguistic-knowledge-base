from os import listdir
from os.path import basename, join
from shutil import copyfile
from tempfile import TemporaryDirectory

from editor import editor

from dictionary.constants import Keys
from dictionary.helpers import saveToFile, openDictionary, readTexts, mergeDicts, readTextsFromDir, \
    saveTextToTempDir


class Dictionary:
    def __init__(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__tempDir = TemporaryDirectory()

    def addTexts(self, filenames):
        for filename in filenames:
            tempFilename = join(self.__tempDir.name, basename(filename))
            copyfile(filename, tempFilename)
        textsData = readTexts(filenames)
        self.__dictionary = mergeDicts(self.__dictionary, textsData)

    def editText(self, filename):
        editor(filename=join(self.__tempDir.name, filename))
        self.__dictionary = readTextsFromDir(self.__tempDir.name)

    @property
    def textsNames(self):
        return listdir(self.__tempDir.name)

    @property
    def tableRecords(self):
        return [[key, value[Keys.occurrence.value]] for key, value in self.__dictionary.items()]

    def save(self, filename=None):
        if filename:
            self.__currentFilename = filename

        texts = []
        for textName in self.textsNames:
            filePath = join(self.__tempDir.name, textName)
            texts.append({
                'name': textName,
                'content': open(filePath, 'r').read(),
            })
        data = {
            'data': self.__dictionary,
            'texts': texts,
        }
        saveToFile(self.__currentFilename, data)

    def readFromFile(self, filename):
        self.__tempDir = TemporaryDirectory()
        self.__dictionary, texts = openDictionary(filename)
        for textData in texts:
            saveTextToTempDir(textData, self.__tempDir.name)
        self.__currentFilename = filename

    def clear(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__tempDir.cleanup()

    def editWord(self, oldWord, newWord):
        newWordData = self.__dictionary.get(newWord)
        if newWordData is None:
            newWordData = {Keys.occurrence.value: 0}
        newWordData[Keys.occurrence.value] += self.__dictionary[oldWord][Keys.occurrence.value]
        self.__dictionary[newWord] = newWordData
        self.__dictionary.pop(oldWord)
