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
        self.verticalLayoutButtons = QtWidgets.QVBoxLayout()
        self.verticalLayoutButtons.setSpacing(10)
        self.verticalLayoutButtons.setObjectName("verticalLayoutButtons")
        self.pushButtonAdd = QtWidgets.QPushButton(parent=self.topWidget)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.verticalLayoutButtons.addWidget(self.pushButtonAdd)
        self.pushButtonEditTags = QtWidgets.QPushButton(parent=self.topWidget)
        self.pushButtonEditTags.setObjectName("pushButtonEditTags")
        self.verticalLayoutButtons.addWidget(self.pushButtonEditTags)
        self.pushButtonSortTags = QtWidgets.QPushButton(parent=self.topWidget)
        self.pushButtonSortTags.setObjectName("pushButtonSortTags")
        self.verticalLayoutButtons.addWidget(self.pushButtonSortTags)
        self.comboBoxSortTasks = QtWidgets.QComboBox(parent=self.topWidget)
        self.comboBoxSortTasks.setObjectName("comboBoxSortTasks")
        self.comboBoxSortTasks.addItem("")
        self.comboBoxSortTasks.addItem("")
        self.verticalLayoutButtons.addWidget(self.comboBoxSortTasks)
        self.comboBoxSortDirection = QtWidgets.QComboBox(parent=self.topWidget)
        self.comboBoxSortDirection.setObjectName("comboBoxSortDirection")
        self.comboBoxSortDirection.addItem("")
        self.comboBoxSortDirection.addItem("")
        self.verticalLayoutButtons.addWidget(self.comboBoxSortDirection)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayoutButtons.addItem(spacerItem)
        self.pushButtonPush = QtWidgets.QPushButton(parent=self.topWidget)
        self.pushButtonPush.setObjectName("pushButtonPush")
        self.verticalLayoutButtons.addWidget(self.pushButtonPush)
        self.pushButtonPull = QtWidgets.QPushButton(parent=self.topWidget)
        self.pushButtonPull.setObjectName("pushButtonPull")
        self.verticalLayoutButtons.addWidget(self.pushButtonPull)
        self.pushButtonSettings = QtWidgets.QPushButton(parent=self.topWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSettings.sizePolicy().hasHeightForWidth())
        self.pushButtonSettings.setSizePolicy(sizePolicy)
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.verticalLayoutButtons.addWidget(self.pushButtonSettings)
        self.gridLayout.addLayout(self.verticalLayoutButtons, 0, 0, 1, 1)
        self.scrollAreaTodos = QtWidgets.QScrollArea(parent=self.topWidget)
        self.scrollAreaTodos.setWidgetResizable(True)
        self.scrollAreaTodos.setObjectName("scrollAreaTodos")
        self.scrollAreaTodosContents = QtWidgets.QWidget()
        self.scrollAreaTodosContents.setGeometry(QtCore.QRect(0, 0, 649, 774))
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
        self.gridLayout.addWidget(self.scrollAreaTodos, 0, 2, 1, 1)
        self.frameTagsList = QtWidgets.QFrame(parent=self.topWidget)
        self.frameTagsList.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameTagsList.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameTagsList.setObjectName("frameTagsList")
        self.gridLayoutFrameTagsList = QtWidgets.QGridLayout(self.frameTagsList)
        self.gridLayoutFrameTagsList.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutFrameTagsList.setObjectName("gridLayoutFrameTagsList")
        self.listWidgetTags = QtWidgets.QListWidget(parent=self.frameTagsList)
        self.listWidgetTags.setStyleSheet("font: 14pt \"Noto Sans\";")
        self.listWidgetTags.setObjectName("listWidgetTags")
        item = QtWidgets.QListWidgetItem()
        self.listWidgetTags.addItem(item)
        self.gridLayoutFrameTagsList.addWidget(self.listWidgetTags, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frameTagsList, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 8)
        MainWindow.setCentralWidget(self.topWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonAdd.setText(_translate("MainWindow", "New Todo"))
        self.pushButtonEditTags.setText(_translate("MainWindow", "Edit Tags"))
        self.pushButtonSortTags.setText(_translate("MainWindow", "Sort Tags"))
        self.comboBoxSortTasks.setItemText(0, _translate("MainWindow", "Due Date"))
        self.comboBoxSortTasks.setItemText(1, _translate("MainWindow", "Tag"))
        self.comboBoxSortDirection.setItemText(0, _translate("MainWindow", "Ascending"))
        self.comboBoxSortDirection.setItemText(1, _translate("MainWindow", "Descending"))
        self.pushButtonPush.setText(_translate("MainWindow", "Push to Server"))
        self.pushButtonPull.setText(_translate("MainWindow", "Pull from Server"))
        self.pushButtonSettings.setText(_translate("MainWindow", "Settings"))
        __sortingEnabled = self.listWidgetTags.isSortingEnabled()
        self.listWidgetTags.setSortingEnabled(False)
        item = self.listWidgetTags.item(0)
        item.setText(_translate("MainWindow", "All Tasks"))
        self.listWidgetTags.setSortingEnabled(__sortingEnabled)
