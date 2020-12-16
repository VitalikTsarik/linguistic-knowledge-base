import nltk
from PyQt5.QtWidgets import QDialog

from gui.gen.search import Ui_searchDialog


class Search(QDialog, Ui_searchDialog):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.files = files
        self.word = ''
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.pushButton.clicked.connect(self.__onSearch)

    def __onSearch(self):
        texts = []
        for file in self.files:
            texts.append(open(file, 'r').read())
        raw_text = '\n'.join(texts)
        word = self.lineEdit.text()
        text = nltk.Text(nltk.word_tokenize(raw_text))
        matches = text.concordance_list(word, width=60)

        lines = []
        for match in matches:
            lines.append(
                f'<span style="color:#7c7c7c;">...{match.left_print} </span>{match.query}<span style="color:#7c7c7c;"> {match.right_print}...</span>')

        # lines = [match.line for match in matches]
        result = '<br/>'.join(lines)
        self.textBrowser.setText(result)


def showSearchDialog(files, parent):
    dialog = Search(files, parent)
    dialog.exec_()
