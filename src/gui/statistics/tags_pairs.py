from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from dictionary.helpers import getAvailableTags
from dictionary.statistics import getTagsPairsStat
from gui.gen.statistics.tags_pairs import Ui_Dialog


class TagsPairs(QDialog, Ui_Dialog):
    def __init__(self, parent, filenames):
        super().__init__(parent)
        self.setupUi(self)

        tags = getAvailableTags()
        for index, tag in enumerate(tags):
            self.tableWidget.insertRow(index)
            self.tableWidget.insertColumn(index)

        self.tableWidget.setHorizontalHeaderLabels(tags)
        self.tableWidget.setVerticalHeaderLabels(tags)

        data = getTagsPairsStat(filenames)
        for rowIndex, (leftTag, rightTags) in enumerate(data.items()):
            for columnIndex, (_, count) in enumerate(rightTags.items()):
                self.tableWidget.setItem(rowIndex, columnIndex, QTableWidgetItem(str(count)))


dialog = None


def showTagsPairs(parent, filenames):
    global dialog
    if dialog is not None:
        dialog.close()
    dialog = TagsPairs(parent, filenames)
    dialog.show()
