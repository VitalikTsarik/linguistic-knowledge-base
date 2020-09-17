import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from dictionary.dictionary_model import DictionaryModel
from dictionary.helpers import read_processed_texts
from gui.gen.main_window import Ui_MainWindow


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)
        dictionary = read_processed_texts()
        records = [[key, value] for key, value in dictionary.items()]
        self.model = DictionaryModel(records=records)
        self.tableView.setModel(self.model)


def main():
    app = QApplication(sys.argv)
    form = App()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
