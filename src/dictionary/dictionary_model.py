import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget

from dictionary.constants import Columns

HEADERS = ['Word', 'Occurrence']

columnSortMap = {
    Columns.word.value: lambda record: record[0].lower(),
    Columns.occurrence.value: lambda record: record[1],
}


class DictionaryModel(QAbstractTableModel):
    def __init__(self, *args, records=None, order=Qt.DescendingOrder, **kwargs):
        super(DictionaryModel, self).__init__(*args, **kwargs)
        self.__records = records or []
        self.__searchPrefix = ''
        self.__searchedRecords = None
        self.sort(Columns.word, order)

    @property
    def records(self):
        return self.__records if self.__searchedRecords is None else self.__searchedRecords

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            return self.records[index.row()][index.column()]

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        self.layoutAboutToBeChanged.emit()
        self.records.sort(key=columnSortMap.get(column), reverse=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        self.layoutAboutToBeChanged.emit()
        self.__records[index.row()][index.column()] = value
        self.layoutChanged.emit()
        return True

    def updateRecords(self, newRecords):
        self.layoutAboutToBeChanged.emit()
        self.__records = newRecords
        self.searchRecords(self.__searchPrefix)
        self.layoutChanged.emit()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.records)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return HEADERS[section]
        return super().headerData(section, orientation, role)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == Columns.word:
            flags |= Qt.ItemIsEditable
        return flags

    def searchRecords(self, prefix):
        self.layoutAboutToBeChanged.emit()
        self.__searchPrefix = prefix
        if prefix == '':
            self.__searchedRecords = None
        else:
            self.__searchedRecords = [rec for rec in self.__records if
                                      rec[Columns.word.value].lower().startswith(prefix)]
        self.layoutChanged.emit()


class ItemDelegate(QStyledItemDelegate):
    itemEdited = pyqtSignal(str, QModelIndex)

    def destroyEditor(self, editor, index: QModelIndex):
        super(ItemDelegate, self).destroyEditor(editor, index)

    def setModelData(self, editor: QWidget, model: DictionaryModel, index: QModelIndex) -> None:
        word = model.records[index.row()][Columns.word]
        super(ItemDelegate, self).setModelData(editor, model, index)
        self.itemEdited.emit(word, index)
