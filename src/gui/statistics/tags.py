from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from dictionary.statistics import getTagsStat
from gui.gen.statistics.two_column_stat_window import Ui_twoColumnStatWindow


class Tags(QDialog, Ui_twoColumnStatWindow):
    def __init__(self, parent, filenames):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Tags Statistic')
        self.tableWidget.setHorizontalHeaderLabels(['Tag', 'Count'])

        tags = getTagsStat(filenames)
        tableRecords = [[tag, count] for tag, count in tags.items()]
        for index, record in enumerate(tableRecords):
            self.tableWidget.insertRow(index)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(record[0]))
            item = QTableWidgetItem()
            item.setData(Qt.EditRole, record[1])
            self.tableWidget.setItem(index, 1, item)


dialog = None


def showTags(parent, filenames):
    global dialog
    if dialog is not None:
        dialog.close()
    dialog = Tags(parent, filenames)
    dialog.show()
