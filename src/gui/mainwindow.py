# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(956, 794)
        self.topWidget = QtWidgets.QWidget(parent=MainWindow)
        self.topWidget.setObjectName("topWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.topWidget)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frameToolbarTags = QtWidgets.QFrame(parent=self.topWidget)
        self.frameToolbarTags.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameToolbarTags.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameToolbarTags.setObjectName("frameToolbarTags")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frameToolbarTags)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonSortTags = QtWidgets.QPushButton(parent=self.frameToolbarTags)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSortTags.sizePolicy().hasHeightForWidth())
        self.pushButtonSortTags.setSizePolicy(sizePolicy)
        self.pushButtonSortTags.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButtonSortTags.setObjectName("pushButtonSortTags")
        self.gridLayout_3.addWidget(self.pushButtonSortTags, 0, 2, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(parent=self.frameToolbarTags)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAdd.setSizePolicy(sizePolicy)
        self.pushButtonAdd.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout_3.addWidget(self.pushButtonAdd, 0, 1, 1, 1)
        self.comboBoxSortTasks = QtWidgets.QComboBox(parent=self.frameToolbarTags)
        self.comboBoxSortTasks.setObjectName("comboBoxSortTasks")
        self.comboBoxSortTasks.addItem("")
        self.comboBoxSortTasks.addItem("")
        self.gridLayout_3.addWidget(self.comboBoxSortTasks, 0, 3, 1, 1)
        self.comboBoxSortDirection = QtWidgets.QComboBox(parent=self.frameToolbarTags)
        self.comboBoxSortDirection.setObjectName("comboBoxSortDirection")
        self.comboBoxSortDirection.addItem("")
        self.comboBoxSortDirection.addItem("")
        self.gridLayout_3.addWidget(self.comboBoxSortDirection, 0, 4, 1, 1)
        self.gridLayout.addWidget(self.frameToolbarTags, 0, 0, 1, 1)
        self.frameBody = QtWidgets.QFrame(parent=self.topWidget)
        self.frameBody.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameBody.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameBody.setObjectName("frameBody")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameBody)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frameTagsList = QtWidgets.QFrame(parent=self.frameBody)
        self.frameTagsList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frameTagsList.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameTagsList.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameTagsList.setObjectName("frameTagsList")
        self.gridLayoutFrameTagsList = QtWidgets.QGridLayout(self.frameTagsList)
        self.gridLayoutFrameTagsList.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutFrameTagsList.setSpacing(0)
        self.gridLayoutFrameTagsList.setObjectName("gridLayoutFrameTagsList")
        self.listWidgetTags = QtWidgets.QListWidget(parent=self.frameTagsList)
        self.listWidgetTags.setStyleSheet("font: 14pt \"Noto Sans\";")
        self.listWidgetTags.setObjectName("listWidgetTags")
        self.gridLayoutFrameTagsList.addWidget(self.listWidgetTags, 0, 0, 1, 1)
        self.pushButtonCompleted = QtWidgets.QPushButton(parent=self.frameTagsList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCompleted.sizePolicy().hasHeightForWidth())
        self.pushButtonCompleted.setSizePolicy(sizePolicy)
        self.pushButtonCompleted.setObjectName("pushButtonCompleted")
        self.gridLayoutFrameTagsList.addWidget(self.pushButtonCompleted, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameTagsList, 0, 0, 1, 1)
        self.scrollAreaTodos = QtWidgets.QScrollArea(parent=self.frameBody)
        self.scrollAreaTodos.setWidgetResizable(True)
        self.scrollAreaTodos.setObjectName("scrollAreaTodos")
        self.scrollAreaTodosContents = QtWidgets.QWidget()
        self.scrollAreaTodosContents.setGeometry(QtCore.QRect(0, 0, 729, 653))
        self.scrollAreaTodosContents.setObjectName("scrollAreaTodosContents")
        self.gridLayoutScrollAreaTodosContent = QtWidgets.QGridLayout(self.scrollAreaTodosContents)
        self.gridLayoutScrollAreaTodosContent.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutScrollAreaTodosContent.setObjectName("gridLayoutScrollAreaTodosContent")
        self.todosFrame = QtWidgets.QFrame(parent=self.scrollAreaTodosContents)
        self.todosFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.todosFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.todosFrame.setObjectName("todosFrame")
        self.verticalLayoutTodosFrame = QtWidgets.QVBoxLayout(self.todosFrame)
        self.verticalLayoutTodosFrame.setObjectName("verticalLayoutTodosFrame")
        self.gridLayoutScrollAreaTodosContent.addWidget(self.todosFrame, 0, 0, 1, 1)
        self.scrollAreaTodos.setWidget(self.scrollAreaTodosContents)
        self.gridLayout_2.addWidget(self.scrollAreaTodos, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frameBody, 1, 0, 1, 1)
        self.frameToolbarSettings = QtWidgets.QFrame(parent=self.topWidget)
        self.frameToolbarSettings.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameToolbarSettings.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameToolbarSettings.setObjectName("frameToolbarSettings")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frameToolbarSettings)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButtonSync = QtWidgets.QPushButton(parent=self.frameToolbarSettings)
        self.pushButtonSync.setObjectName("pushButtonSync")
        self.gridLayout_4.addWidget(self.pushButtonSync, 0, 4, 1, 1)
        self.pushButtonEditTags = QtWidgets.QPushButton(parent=self.frameToolbarSettings)
        self.pushButtonEditTags.setObjectName("pushButtonEditTags")
        self.gridLayout_4.addWidget(self.pushButtonEditTags, 0, 2, 1, 1)
        self.pushButtonSettings = QtWidgets.QPushButton(parent=self.frameToolbarSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSettings.sizePolicy().hasHeightForWidth())
        self.pushButtonSettings.setSizePolicy(sizePolicy)
        self.pushButtonSettings.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.gridLayout_4.addWidget(self.pushButtonSettings, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 1, 1, 1)
        self.pushButtonRefresh = QtWidgets.QPushButton(parent=self.frameToolbarSettings)
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.gridLayout_4.addWidget(self.pushButtonRefresh, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frameToolbarSettings, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.topWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonSortTags.setText(_translate("MainWindow", "Sort Tags"))
        self.pushButtonAdd.setText(_translate("MainWindow", "New Todo"))
        self.comboBoxSortTasks.setItemText(0, _translate("MainWindow", "Due Date"))
        self.comboBoxSortTasks.setItemText(1, _translate("MainWindow", "Tag"))
        self.comboBoxSortDirection.setItemText(0, _translate("MainWindow", "Ascending"))
        self.comboBoxSortDirection.setItemText(1, _translate("MainWindow", "Descending"))
        self.pushButtonCompleted.setText(_translate("MainWindow", "Completed"))
        self.pushButtonSync.setText(_translate("MainWindow", "Sync With Server"))
        self.pushButtonEditTags.setText(_translate("MainWindow", "Edit Tags"))
        self.pushButtonSettings.setText(_translate("MainWindow", "Settings"))
        self.pushButtonRefresh.setText(_translate("MainWindow", "Refresh Table"))
