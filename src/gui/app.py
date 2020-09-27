import sys

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from constants import DICTIONARIES_PATH, TEXTS_PATH
from dictionary.dictionary_model import DictionaryModel, ItemDelegate, Columns
from dictionary.helpers import readTexts, mergeDicts, saveDictionary, openDictionary
from gui.gen.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.__dictionary = {}
        self.__currentDictionaryFile = None
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.__initMenu()
        self.__initTable()

    def __initMenu(self):
        self.actionAddText.triggered.connect(self.__onAddText)
        self.actionOpen.triggered.connect(self.__onOpen)
        self.actionSave.setDisabled(True)
        self.actionSave.triggered.connect(self.__onSave)
        self.actionSaveAs.triggered.connect(self.__onSaveAs)
        self.actionClose.triggered.connect(self.__onClose)

    def __initTable(self):
        self.tableView.setItemDelegate(ItemDelegate(self))
        self.tableView.itemDelegate().itemEdited.connect(self.__onItemEdited)

    def __updateTable(self):
        records = [[key, value] for key, value in self.__dictionary.items()]
        self.tableView.setModel(DictionaryModel(records=records))

    def __onAddText(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', TEXTS_PATH, 'Text Files (*.txt)')
        if len(filenames):
            textsData = readTexts(filenames)
            self.__dictionary = mergeDicts(self.__dictionary, textsData)
            self.__updateTable()

    def __onSaveAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            if not filename.endswith('.dict'):
                filename += '.dict'
            saveDictionary(filename, self.__dictionary)
            self.__currentDictionaryFile = filename
            self.actionSave.setDisabled(False)

    def __onSave(self):
        saveDictionary(self.__currentDictionaryFile, self.__dictionary)

    def __onOpen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            self.__dictionary = openDictionary(filename)
            self.__currentDictionaryFile = filename
            self.actionSave.setDisabled(False)
            self.__updateTable()

    def __onClose(self):
        self.__dictionary = {}
        self.__currentDictionaryFile = None
        self.actionSave.setDisabled(True)
        self.__updateTable()

    def __onItemEdited(self, word, index: QModelIndex):
        if index.column() == Columns.word.value:
            self.__dictionary[index.data()] = self.__dictionary.setdefault(index.data(), 0) + self.__dictionary[word]
            self.__dictionary.pop(word)
            self.__updateTable()
        elif index.column() == Columns.occurrence.value:
            self.__dictionary[word] = str(index.data())


def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
