import sys
from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from davconnect import *
from fileutils import *
from syncutils import *
from gui.edittask import *
from gui.mainwindow import Ui_MainWindow
from gui.settingsdialog import Ui_DialogSettings



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        # loadUi("mainwindow.ui", self)
        self.setWindowTitle("DAV Tasks")
        
        self.uidMover = None

        self.populateTags()
        self.populateTable()

        self.pushButtonRefresh.clicked.connect(self.pullLocalData)
        self.pushButtonAdd.clicked.connect(self.taskDialog)
        self.pushButtonSettings.clicked.connect(self.settingsDialog)
        self.pushButtonSync.clicked.connect(self.pullUpstreamData)
        self.pushButtonClear.clicked.connect(self.clearMainWindow)
        
        

    def populateTable(self):
        readLocalFile("todos")
        todos = readLocalFile.data
        i = 0

        for t in todos.values():
            uid = t["UID"]
            summary = t["SUMMARY"]

            if "DUE;TZID=America/New_York" in t.keys():
                rawDate = t["DUE;TZID=America/New_York"]
                print(rawDate)
            else:
                rawDate = None

            self.frameTodo = QtWidgets.QWidget(self.todosFrame)
            self.frameTodo.setStyleSheet("background-color: rgb(51, 51, 51);")
            self.frameTodo.setObjectName(uid)
            self.frameTodo.setMinimumSize(QtCore.QSize(0, 40))
            self.frameTodo.setMaximumSize(QtCore.QSize(16777215, 50))

            self.gridLayoutTodo = QtWidgets.QGridLayout(self.frameTodo)
            self.gridLayoutTodo.setContentsMargins(0, 0, 0, 0)

            self.frameTag = QtWidgets.QFrame()
            self.frameTag.setStyleSheet("background-color: rgb(90, 90, 90);")
            self.gridLayoutTodo.addWidget(self.frameTag, 0, 0, 1, 1)

            self.labelTag = QtWidgets.QLabel(self.frameTag)
            self.labelTag.setMargin(10)

            if "CATEGORIES" in t:
                tag = t["CATEGORIES"]
                self.labelTag.setText(tag)

            self.frameSummary = QtWidgets.QFrame()
            self.gridLayoutSummary = QtWidgets.QGridLayout(self.frameSummary)
            self.gridLayoutSummary.setSpacing(0)
            self.gridLayoutTodo.addWidget(self.frameSummary, 0, 1, 1, 1)

            self.labelSummary = QtWidgets.QLabel()
            self.labelSummary.setText(summary)
            self.labelSummary.setWordWrap(True)
            self.labelSummary.setContentsMargins(0, 0, 0, 0)
            self.labelSummary.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
            self.gridLayoutSummary.addWidget(self.labelSummary, 0, 0, 1, 1)

            self.frameDuedays = QtWidgets.QFrame()
            self.gridLayoutTodo.addWidget(self.frameDuedays, 0, 2, 1, 1)

            self.labelCountdown = QtWidgets.QLabel(self.frameDuedays)
            self.labelCountdown.setStyleSheet("color: rgb(0, 0, 0);")
            self.labelCountdown.setMargin(1)
            self.labelCountdown.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter)

            self.frameDate = QtWidgets.QFrame()
            self.gridLayoutTodo.addWidget(self.frameDate, 0, 3, 1, 1)

            self.frameEdit = QtWidgets.QFrame()
            self.frameEdit.setStyleSheet("background-color: rgb(58, 58, 58);")
            self.gridLayoutTodo.addWidget(self.frameEdit, 0, 4, 1, 1)

            self.pushButtonEdit = QtWidgets.QPushButton(self.frameEdit)
            self.pushButtonEdit.setText("\U0001F5D1")
            self.pushButtonEdit.clicked.connect(self.taskDialog)
            self.pushButtonEdit.setObjectName("pushButtonEdit_" + uid)

            self.gridLayoutTodo.setColumnStretch(0, 1)
            self.gridLayoutTodo.setColumnStretch(1, 5)
            self.gridLayoutTodo.setColumnStretch(2, 1)
            self.gridLayoutTodo.setColumnStretch(3, 1)
            self.gridLayoutTodo.setColumnStretch(4, 1)

            if rawDate == None:
                self.frameDuedays.setStyleSheet(
                    "background-color: rgb(51, 51, 51);")
                self.labelCountdown.setStyleSheet("color: rgb(51, 51, 51);")

            else:
                formattedDate = formatDateNormal(rawDate)
                today = date.today()
                delta = formattedDate - today
                self.labelCountdown.setText(str(delta.days))
                if delta.days < 1 and delta.days >= 0:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(204, 51, 0);")
                if delta.days > 1 and delta.days <= 2:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(255, 153, 102);")
                if delta.days > 2 and delta.days <= 3:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(255, 204, 0);")
                if delta.days > 3 and delta.days <= 30:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(51, 153, 0);")
                if delta.days > 30:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(51, 153, 0);")
                    self.labelCountdown.setText("30+")
                if delta.days < 0:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(204, 51, 0);")
                    self.labelCountdown.setText("Overdue")
                self.labelDate = QtWidgets.QLabel(self.frameDate)
                self.labelDate.setText(
                    str(formattedDate.month) + "-" + str(formattedDate.day))
                self.labelDate.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

            self.verticalLayoutTodosFrame.addWidget(self.frameTodo)

            i = i + 1
        print("populateTable")

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        item = QListWidgetItem()
        for t in tags:
            if type(t) == dict:
                self.listWidgetTags.addItem("No Data")
            else:
                item.setText(t)
                item.setForeground(QColor().black())

                if len(tags[t]) != 0:
                    item.setBackground(QColor(tags[t]))
                self.listWidgetTags.addItem(item)
        print("populateTags")

        
    def clearMainWindow(self):
        self.listWidgetTags.clear()
        if self.uidMover != None:
            widget = self.todosFrame.findChild(QWidget, self.uidMover)
            if widget != None:
                widget.setParent(None)
                widget.deleteLater()
            self.uidMover = None
            print("clearMainWindow - SingleTask")
        
        else:
            readLocalFile("todos")
            todos = readLocalFile.data

            for t in todos.values():
                uid = t["UID"]
                widget = self.todosFrame.findChild(QWidget, uid)
                if widget != None:
                    widget.setParent(None)
                    widget.deleteLater()
                    print("clearMainWindow")
        
        self.todosFrame.update()
        

    def pullUpstreamData(self):
        compareData()
        self.clearMainWindow()
        self.populateTags()
        self.populateTable()
        print("pullUpstreamData")

    def pullLocalData(self):
        self.clearMainWindow()
        self.populateTags()
        self.populateTable()
        print("pullLocalData")

    def settingsDialog(self):
        print("settingsDialog opened")
        dlg = SettingsDialog()
        if dlg.exec():
            n = 0
        else:
            print("settingsDialog closed")

    def taskDialog(self):
        
        if self.sender().objectName() == "pushButtonAdd":
            print("taskDialog opened to add")
            dlg = TaskDialog(None)
        else:
            print("taskDialog opened to edit")
            uid = self.sender().objectName()[15:]
            self.uidMover = uid
            dlg = TaskDialog(uid)
    
        if dlg.exec():
            self.clearMainWindow()
        else:
            print("")
            
class SettingsDialog(QDialog, Ui_DialogSettings):
    def __init__(self, *args, obj=None, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.populateTags()
        self.populateForm()

        self.pushButtonTest.clicked.connect(self.onColorPicker)
        self.pushButtonTagApply.clicked.connect(self.saveTagColor)

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        for t in tags:
            self.comboBoxTags.addItem(t)

    def populateForm(self):
        readLocalFile("settings")
        settings = readLocalFile.data
        if settings["URL"] != "":
            self.lineEditURL.setText(settings["URL"])

        if settings["USERNAME"] != "":
            self.lineEditUser.setText(settings["USERNAME"])

        if settings["PASSWORD"] != "":
            self.lineEditPass.setText(settings["PASSWORD"])

    def onColorPicker(self):
        color = QColorDialog.getColor()
        self.widgetColorPreview.setStyleSheet(
            "background-color:" + color.name() + ";")
        self.widgetColorPreview.setObjectName(color.name())

    def saveServerSettings(self):
        newSettings = {
            "URL": "",
            "USERNAME": "",
            "PASSWORD": ""
        }

    def saveTagColor(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        inputTag = self.comboBoxTags.currentText()
        newSettings = {}
        for x, y in tags.items():
            if x == inputTag:
                newSettings[x] = self.widgetColorPreview.objectName()
        changeLocalData(newSettings, "tags")
        super(SettingsDialog, self).reject()

    def removeTagColor(self):
        n = 0


class TaskDialog(QDialog, Ui_EditTaskDialog):
    def __init__(self, uid, *args, obj=None, **kwargs):
        super(TaskDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        saveButton = QPushButton("Save")
        deleteButton = QPushButton("Delete")
        applyButton = QPushButton("Apply")
        
        if uid == None:
            self.buttonBox.addButton(saveButton, self.buttonBox.ButtonRole.YesRole)
            self.populateTags()
        else:
            self.buttonBox.addButton(deleteButton, self.buttonBox.ButtonRole.DestructiveRole)
            self.buttonBox.addButton(applyButton, self.buttonBox.ButtonRole.ApplyRole)
            self.populateForm(uid)
            self.populateTags()
            
        self.checkBoxEnableCalendar.toggled.connect(self.toggleDatePicker)
        saveButton.clicked.connect(self.submitTodo)
        deleteButton.clicked.connect(lambda: self.deleteTodo(uid))
        applyButton.clicked.connect(self.applyEdits)
    
    def applyEdits(self):
        print("- applyEdits")
        self.accept()
        
    def deleteTodo(self, uid):
        print("- deleteTodo")
        print(uid)
        # deleteTodoByUID(uid)
        self.accept()

    def submitTodo(self, uid):
                 
        if not self.comboBoxTags.currentText():
            tag = None
        else:
            tag = self.comboBoxTags.currentText()
            
        if self.dateEdit.isEnabled():
            createTodo(tag, self.lineEditSummary.text(), self.dateEdit.date(), uid)
        else:
            createTodo(tag, self.lineEditSummary.text(), None, uid)
                
        print("- submitTodo")
        self.accept()

    def toggleDatePicker(self):
        if self.dateEdit.isEnabled():
            self.dateEdit.setEnabled(False)
        else:
            self.dateEdit.setEnabled(True)

    def populateForm(self, uid):

        readLocalFile("todos")
        todos = readLocalFile.data
        i = 0
        keyUID = "UID"
        keyCat = "CATEGORIES"

        for t in todos.values():
            if keyUID in t.keys():
                if t[keyUID] == uid:

                    if "DUE" in t.keys():
                        currentDueRaw = t["DUE"]
                        currentDue = formatDateNormal(currentDueRaw)
                    else:
                        currentDue = None

                    if "CATEGORIES" in t.keys():
                        self.comboBoxTags.setCurrentText(t["CATEGORIES"])

                    if currentDue == None:
                        self.dateEdit.setDate(date.today())
                        self.dateEdit.setEnabled(False)
                        self.checkBoxEnableCalendar.setChecked(False)
                    else:
                        self.checkBoxEnableCalendar.setChecked(True)
                        self.dateEdit.setEnabled(True)
                        self.dateEdit.setDate(currentDue)

                    self.lineEditSummary.setText(t["SUMMARY"])

            else:
                null = 0
        print("- populateForm")

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        for t in tags:
            self.comboBoxTags.addItem(t)
        print("- populateTags")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
