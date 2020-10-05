from PyQt5.QtWidgets import QDialog

from gui.gen.add_word_dialog import Ui_AddWordDialog


class AddWordDialog(QDialog, Ui_AddWordDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.word = ''
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.buttonBox.accepted.connect(self.__onAccept)

    def __onAccept(self):
        self.word = self.wordLineEdit.text()


def showAddWordDialog(parent):
    dialog = AddWordDialog(parent)
    if dialog.exec_():
        return dialog.word
