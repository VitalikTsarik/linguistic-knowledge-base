import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

from dictionary.dictionary_model import DictionaryModel
from dictionary.helpers import readTexts, mergeDicts
from gui.gen.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.__dictionary = {}
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.actionAddText.triggered.connect(self.__onAddText)
        self.actionClose.triggered.connect(self.__onClose)

    def __updateTable(self):
        records = [[key, value] for key, value in self.__dictionary.items()]
        self.tableView.setModel(DictionaryModel(records=records))

    def __onAddText(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', '', 'Text Files (*.txt)')
        if len(filenames):
            print(filenames)
            textsData = readTexts(filenames)
            self.__dictionary = mergeDicts(self.__dictionary, textsData)
            self.__updateTable()

    def __onClose(self):
        self.__dictionary = {}
        self.__updateTable()


def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
