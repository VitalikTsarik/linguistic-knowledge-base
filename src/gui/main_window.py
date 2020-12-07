from os.path import basename

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QAction

from constants import DICTIONARIES_PATH, TEXTS_PATH
from dictionary.dictionary import Dictionary
from dictionary.dictionary_table_model import DictionaryTableModel, ItemDelegate, Columns
from gui.dialogs.add_word_dialog import showAddWordDialog
from gui.dialogs.remove_word_confirm import showRemoveWordConfirm
from gui.dialogs.tags_help import showTagsHelp
from gui.gen.main_window import Ui_MainWindow
from gui.statistics.tags_pairs import showTagsPairs
from gui.statistics.word_tag_pairs import showWordTagPairs
from gui.statistics.tags import showTags


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__dictionary = Dictionary()
        self.setupUi(self)
        self.__initUI()

    def __initUI(self):
        self.__initMenu()
        self.__initTable()
        self.searchLineEdit.textEdited.connect(self.__onSearchInput)
        self.addWordButton.clicked.connect(self.__onAddWordBtnClick)
        self.removeWordButton.clicked.connect(self.__onRemoveWordBtnClick)

    def __initMenu(self):
        self.actionAddText.triggered.connect(self.__onAddText)
        self.actionOpen.triggered.connect(self.__onOpen)
        self.actionSave.setDisabled(True)
        self.actionSave.triggered.connect(self.__onSave)
        self.actionSaveAs.triggered.connect(self.__onSaveAs)
        self.actionClose.triggered.connect(self.__onClose)
        self.menuEditText.setDisabled(True)
        self.menuEditTaggedText.setDisabled(True)
        self.actionTags.triggered.connect(self.__onTagsHelp)
        self.actionStatTags.triggered.connect(self.__onStatTags)
        self.actionStatWordTagPairs.triggered.connect(self.__onStatWordTagPairs)
        self.actionStatTagsPairs.triggered.connect(self.__onStatTagsPairs)

    def __initTable(self):
        self.tableView.setItemDelegate(ItemDelegate(self))
        self.tableView.itemDelegate().itemEdited.connect(self.__onItemEdited)
        self.tableView.setModel(DictionaryTableModel(records=self.__dictionary.tableRecords))
        self.tableView.selectionModel().selectionChanged.connect(self.__onSelectionChange)
        self.removeWordButton.setDisabled(True)

    def __updateTable(self):
        self.tableView.model().updateRecords(self.__dictionary.tableRecords)
        self.tableView.selectionModel().clearSelection()

    def __onAddText(self):
        filenames, _ = QFileDialog.getOpenFileNames(self, 'Open file', TEXTS_PATH, 'Text Files (*.txt)')
        if len(filenames):
            self.__dictionary.addTexts(filenames)
            self.__updateTable()
            self.__addTextMenuItems(filenames)
            self.__addTaggedTextMenuItems([Dictionary.getTaggedFilename(filename) for filename in filenames])

    def __addTextMenuItems(self, filenames):
        self.menuEditText.setDisabled(False)
        for filename in filenames:
            textName = basename(filename)
            action = QAction(textName, self.menuEditText)
            action.triggered.connect(lambda chk, name=textName: self.__onEditText(name))
            self.menuEditText.addAction(action)

    def __onEditText(self, name):
        self.__dictionary.editText(name)
        self.__updateTable()

    def __addTaggedTextMenuItems(self, filenames):
        self.menuEditTaggedText.setDisabled(False)
        for filename in filenames:
            textName = basename(filename)
            action = QAction(textName, self.menuEditText)
            action.triggered.connect(lambda chk, name=textName: self.__onEditTaggedText(name))
            self.menuEditTaggedText.addAction(action)

    def __onEditTaggedText(self, name):
        self.__dictionary.editTaggedText(name)
        self.__updateTable()

    def __onSaveAs(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            if not filename.endswith('.dict'):
                filename += '.dict'
            self.__dictionary.save(filename)
            self.actionSave.setDisabled(False)

    def __onSave(self):
        self.__dictionary.save()

    def __onOpen(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open dictionary', DICTIONARIES_PATH,
                                                  'Dictionary Files (*.dict)')
        if filename:
            self.__dictionary.open(filename)
            self.__updateTable()

            self.actionSave.setDisabled(False)
            self.menuEditText.clear()
            self.menuEditTaggedText.clear()
            self.__addTextMenuItems(self.__dictionary.textsNames)
            self.__addTaggedTextMenuItems(self.__dictionary.taggedTextsNames)

    def __onClose(self):
        self.__dictionary.close()
        self.__updateTable()

        self.actionSave.setDisabled(True)
        self.menuEditText.setDisabled(True)
        self.menuEditText.clear()
        self.menuEditTaggedText.setDisabled(True)
        self.menuEditTaggedText.clear()

    def __onTagsHelp(self):
        showTagsHelp(self)

    def __onStatTags(self):
        showTags(self, self.__dictionary.taggedTextsTempFilenames)

    def __onStatWordTagPairs(self):
        showWordTagPairs(self, self.__dictionary.textsTempFilenames)

    def __onStatTagsPairs(self):
        showTagsPairs(self, self.__dictionary.textsTempFilenames)

    def __onItemEdited(self, oldValue, index: QModelIndex):
        newValue = index.data()
        if index.column() == Columns.word.value:
            self.__dictionary.editWord(oldValue, newValue)
        elif index.column() == Columns.tags.value:
            word = index.siblingAtColumn(Columns.word.value).data()
            self.__dictionary.editTags(word, newValue)
        elif index.column() == Columns.base.value:
            word = index.siblingAtColumn(Columns.word.value).data()
            self.__dictionary.editBase(word, newValue)
        self.__updateTable()

    def __onAddWordBtnClick(self):
        word = showAddWordDialog(self)
        if word:
            result = self.__dictionary.addWord(word)
            if result:
                self.__updateTable()

    def __onSelectionChange(self):
        self.removeWordButton.setDisabled(not self.tableView.selectionModel().hasSelection())

    def __onRemoveWordBtnClick(self):
        words = []
        for index in self.tableView.selectedIndexes():
            if index.column() == Columns.word.value:
                words.append(index.data())

        result = showRemoveWordConfirm(self, words.copy())
        if result:
            self.__dictionary.removeWords(words)
            self.__updateTable()

    def __onSearchInput(self, text):
        self.tableView.model().searchRecords(text.lower())
