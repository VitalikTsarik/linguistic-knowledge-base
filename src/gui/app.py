import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from dictionary.dictionary_model import DictionaryModel
from dictionary.helpers import readTexts, mergeDicts, saveDictionary
from gui.gen.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.__dictionary = {}
        self.__currentDictionaryFile = None
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.actionAddText.triggered.connect(self.__onAddText)
        self.actionSave.setDisabled(True)
        self.actionSave.triggered.connect(self.__onSave)
        self.actionSaveAs.triggered.connect(self.__onSaveAs)
        self.actionClose.triggered.connect(self.__onClose)

    def __updateTable(self):
        records = [[key, value] for key, value in self.__dictionary.items()]
        self.tableView.setModel(DictionaryModel(records=records))

    def __onAddText(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', '', 'Text Files (*.txt)')
        if len(filenames):
            textsData = readTexts(filenames)
            self.__dictionary = mergeDicts(self.__dictionary, textsData)
            self.__updateTable()

    def __onSaveAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save dictionary', '', 'Dictionary Files (*.dict)')
        if filename:
            if not filename.endswith('.dict'):
                filename += '.dict'
            saveDictionary(filename, self.__dictionary)
            self.__currentDictionaryFile = filename
            self.actionSave.setDisabled(False)

    def __onSave(self):
        saveDictionary(self.__currentDictionaryFile, self.__dictionary)

    def __onClose(self):
        self.__dictionary = {}
        self.__currentDictionaryFile = None
        self.actionSave.setDisabled(True)
        self.__updateTable()


def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
