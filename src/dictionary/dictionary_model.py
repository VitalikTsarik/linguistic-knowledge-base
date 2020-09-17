import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class DictionaryModel(QAbstractTableModel):
    def __init__(self, *args, records=None, **kwargs):
        super(DictionaryModel, self).__init__(*args, **kwargs)
        self.headers = ['Word', 'Occurrence']
        self.__records = records or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.__records[index.row()][index.column()]

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        self.__records.sort(key=lambda record: record[column], reverse=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.__records)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
        return super().headerData(section, orientation, role)
