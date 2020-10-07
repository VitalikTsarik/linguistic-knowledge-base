from PyQt5.QtWidgets import QDialog

from gui.gen.remove_word_confirm import Ui_RemoveWordConfirm


class RemoveWordConfirm(QDialog, Ui_RemoveWordConfirm):
    def __init__(self, parent, words):
        super().__init__(parent)
        self.setupUi(self)
        self.textBrowser.setText(self.__formatWords(words))

    @staticmethod
    def __formatWords(words):
        return ', '.join(words)


def showRemoveWordConfirm(parent, words):
    dialog = RemoveWordConfirm(parent, words)
    if dialog.exec_():
        return dialog.result()
