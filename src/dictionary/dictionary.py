from dictionary.constants import Keys
from dictionary.helpers import saveDictionary, openDictionary, readTexts, mergeDicts


class Dictionary:
    def __init__(self):
        self.__dictionary = {}
        self.__currentFilename = None
        self.__textsFilenames = []

    def addTexts(self, filenames):
        textsData = readTexts(filenames)
        self.__dictionary = mergeDicts(self.__dictionary, textsData)

    @property
    def tableRecords(self):
        return [[key, value[Keys.occurrence.value]] for key, value in self.__dictionary.items()]

    def save(self, filename=None):
        if filename:
            self.__currentFilename = filename
        saveDictionary(self.__currentFilename, self.__dictionary)

    def readFromFile(self, filename):
        self.__dictionary = openDictionary(filename)
        self.__currentFilename = filename

    def clear(self):
        self.__dictionary = {}
        self.__currentFilename = None

    def editWord(self, oldWord, newWord):
        newWordData = self.__dictionary.get(newWord)
        if newWordData is None:
            newWordData = {Keys.occurrence.value: 0}
        newWordData[Keys.occurrence.value] += self.__dictionary[oldWord][Keys.occurrence.value]
        self.__dictionary[newWord] = newWordData
        self.__dictionary.pop(oldWord)
