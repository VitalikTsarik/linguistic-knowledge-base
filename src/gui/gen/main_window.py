# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(976, 878)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(545, 511))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setAutoFillBackground(False)
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableView.setDragDropOverwriteMode(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableView.setShowGrid(True)
        self.tableView.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(200)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.searchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.horizontalLayout.addWidget(self.searchLineEdit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.addWordButton = QtWidgets.QPushButton(self.centralwidget)
        self.addWordButton.setObjectName("addWordButton")
        self.horizontalLayout.addWidget(self.addWordButton)
        self.removeWordButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeWordButton.setObjectName("removeWordButton")
        self.horizontalLayout.addWidget(self.removeWordButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 976, 20))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuText = QtWidgets.QMenu(self.menubar)
        self.menuText.setObjectName("menuText")
        self.menuEditText = QtWidgets.QMenu(self.menuText)
        self.menuEditText.setObjectName("menuEditText")
        self.menuEditTaggedText = QtWidgets.QMenu(self.menuText)
        self.menuEditTaggedText.setObjectName("menuEditTaggedText")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionAddText = QtWidgets.QAction(MainWindow)
        self.actionAddText.setObjectName("actionAddText")
        self.actionTags = QtWidgets.QAction(MainWindow)
        self.actionTags.setObjectName("actionTags")
        self.actionj = QtWidgets.QAction(MainWindow)
        self.actionj.setObjectName("actionj")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addAction(self.actionClose)
        self.menuText.addAction(self.actionAddText)
        self.menuText.addSeparator()
        self.menuText.addAction(self.menuEditText.menuAction())
        self.menuText.addAction(self.menuEditTaggedText.menuAction())
        self.menuHelp.addAction(self.actionTags)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuText.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Search"))
        self.searchLineEdit.setPlaceholderText(_translate("MainWindow", "Start typing a word"))
        self.addWordButton.setText(_translate("MainWindow", "Add"))
        self.removeWordButton.setText(_translate("MainWindow", "Remove"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuText.setTitle(_translate("MainWindow", "Edit"))
        self.menuEditText.setTitle(_translate("MainWindow", "Edit text"))
        self.menuEditTaggedText.setTitle(_translate("MainWindow", "Edit tagged text"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open..."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save as..."))
        self.actionSaveAs.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionAddText.setText(_translate("MainWindow", "Add text..."))
        self.actionAddText.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionTags.setText(_translate("MainWindow", "Tags"))
        self.actionj.setText(_translate("MainWindow", "j"))
