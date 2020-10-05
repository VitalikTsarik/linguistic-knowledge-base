import sys
from os.path import basename

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction

from constants import DICTIONARIES_PATH, TEXTS_PATH
from dictionary.dictionary import Dictionary
from dictionary.dictionary_model import DictionaryModel, ItemDelegate, Columns
from gui.gen.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.__dictionary = Dictionary()
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
        self.__updateTable()

    def __updateTable(self):
        self.tableView.setModel(DictionaryModel(records=self.__dictionary.tableRecords))

    def __onAddText(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', TEXTS_PATH, 'Text Files (*.txt)')
        if len(filenames):
            self.__dictionary.addTexts(filenames)
            self.__updateTable()
            self.__addTextMenuItems(filenames)

    def __addTextMenuItems(self, filenames):
        for filename in filenames:
            textName = basename(filename)
            action = QAction(textName, self.menuEditText)
            action.triggered.connect(lambda chk, name=textName: self.__onEditText(name))
            self.menuEditText.addAction(action)

    def __onEditText(self, name):
        self.__dictionary.editText(name)
        self.__updateTable()

    def __onSaveAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            if not filename.endswith('.dict'):
                filename += '.dict'
            self.__dictionary.save(filename)
            self.actionSave.setDisabled(False)

    def __onSave(self):
        self.__dictionary.save()

    def __onOpen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            self.__dictionary.readFromFile(filename)
            self.__updateTable()

            self.actionSave.setDisabled(False)
            self.menuEditText.setDisabled(False)
            self.menuEditText.clear()
            self.__addTextMenuItems(self.__dictionary.textsNames)

    def __onClose(self):
        self.__dictionary.clear()
        self.__updateTable()

        self.actionSave.setDisabled(True)
        self.menuEditText.setDisabled(True)
        self.menuEditText.clear()

    def __onItemEdited(self, word, index: QModelIndex):
        if index.column() == Columns.word.value:
            self.__dictionary.editWord(word, index.data())
            self.__updateTable()


def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
