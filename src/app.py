import sys

import nltk
from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow

if __name__ == '__main__':
    nltk.download('averaged_perceptron_tagger')
    nltk.download('tagsets')

    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()
