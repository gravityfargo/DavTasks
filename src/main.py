import sys
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from davconnect import *
from fileutils import *
from syncutils import *
from gui.edittask import *
from gui.edittags import *
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

        self.pushButtonAdd.clicked.connect(self.taskDialog)
        self.pushButtonEditTags.clicked.connect(self.editTagsDialog)
        
        # self.pushButtonPush.clicked.connect(self.pullLocalData)
        self.pushButtonPull.clicked.connect(self.pullUpstreamData)
        self.pushButtonSettings.clicked.connect(self.settingsDialog)

    def populateTable(self):
        readLocalFile("todos")
        todos = readLocalFile.data

        readLocalFile("tags")
        tags = readLocalFile.data
        i = 0

        self.verticalLayoutTodosFrame.setSpacing(2)
        for t in todos.values():
            uid = t["UID"]
            summary = t["SUMMARY"]

            if "DUE;TZID=America/New_York" in t.keys():
                rawDate = t["DUE;TZID=America/New_York"]
            elif "DUE" in t.keys():
                rawDate = t["DUE"]
            else:
                rawDate = None

            self.frameTodo = QtWidgets.QWidget(self.todosFrame)
            self.frameTodo.setStyleSheet("background-color: rgb(51, 51, 51);")
            self.frameTodo.setObjectName(uid)
            self.frameTodo.setMinimumSize(QtCore.QSize(0, 50))
            self.frameTodo.setMaximumSize(QtCore.QSize(16777215, 50))

            self.gridLayoutTodo = QtWidgets.QGridLayout(self.frameTodo)
            self.gridLayoutTodo.setContentsMargins(0, 0, 0, 0)

            self.frameTag = QtWidgets.QFrame()
            self.gridLayoutTodo.addWidget(self.frameTag, 0, 0, 1, 1)

            self.gridLayoutTag = QtWidgets.QGridLayout(self.frameTag)
            self.gridLayoutTag.setContentsMargins(0, 0, 0, 0)

            self.frameTagColor = QtWidgets.QFrame()
            self.frameTagColor.setMaximumSize(QtCore.QSize(10, 50))
            self.gridLayoutTag.addWidget(self.frameTagColor, 0, 0, 1, 1)

            self.labelTag = QtWidgets.QLabel()

            self.gridLayoutTag.addWidget(self.labelTag, 0, 1, 1, 1)

            if "CATEGORIES" in t:
                tag = t["CATEGORIES"]
                self.labelTag.setText(tag)
                if tag in tags.keys() and len(tags[tag]) > 0:
                    self.frameTagColor.setStyleSheet(
                        "background-color: " + tags[tag] + ";")

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
            
            self.gridLayoutCountdown = QtWidgets.QGridLayout(self.frameDuedays)
            self.gridLayoutCountdown.setContentsMargins(0, 0, 0, 0)

            self.labelCountdown = QtWidgets.QLabel()
            font = QtGui.QFont()
            font.setBold(True)
            self.labelCountdown.setFont(font)
            self.labelCountdown.setStyleSheet("color: rgb(0, 0, 0); font: 12pt;")
            self.gridLayoutCountdown.addWidget(self.labelCountdown, 0, 0, 1, 1)
            self.labelCountdown.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            
            

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

        self.spacerItem = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayoutTodosFrame.addItem(self.spacerItem)

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data

        for t in tags:
            item = QListWidgetItem()
            item.setText(t)

            if len(tags[t]) != 0:
                item.setForeground(QColor().black())
                item.setBackground(QColor(tags[t]))
            self.listWidgetTags.addItem(item)
        self.listWidgetTags.sortItems(Qt.SortOrder.AscendingOrder)

    def clearMainWindow(self):
        self.listWidgetTags.clear()
        if self.uidMover != None:
            widget = self.todosFrame.findChild(QWidget, self.uidMover)
            if widget != None:
                widget.deleteLater()
            self.uidMover = None

        readLocalFile("todos")
        todos = readLocalFile.data
        for t in todos.values():
            uid = t["UID"]
            widget = self.todosFrame.findChild(QWidget, uid)
            if widget != None:
                widget.deleteLater()

        self.verticalLayoutTodosFrame.removeItem(self.spacerItem)
        self.todosFrame.update()

    def pullUpstreamData(self):
        self.clearMainWindow()
        compareData()
        self.populateTags()
        self.populateTable()

    def pullLocalData(self):
        self.clearMainWindow()
        self.populateTags()
        self.populateTable()

    def editTagsDialog(self):
        dlg = EditTagsDialog()
        if dlg.exec():
            self.pullLocalData()

    def settingsDialog(self):
        dlg = SettingsDialog()
        dlg.exec()

    def taskDialog(self):

        if self.sender().objectName() == "pushButtonAdd":
            dlg = TaskDialog(None)
        else:
            uid = self.sender().objectName()[15:]
            self.uidMover = uid
            dlg = TaskDialog(uid)

        if dlg.exec():
            self.pullLocalData()


class EditTagsDialog(QDialog, Ui_EditTagDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(EditTagsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        readLocalFile("tags")

        self.tags = readLocalFile.data
        self.pushButtonColorPicker.clicked.connect(self.onColorPicker)
        self.buttonBox.accepted.connect(self.saveTagColor)
        self.populateTags()
        self.setPreviewColor(self.comboBoxTags.currentText())
        self.comboBoxTags.currentTextChanged.connect(
            lambda: self.setPreviewColor(self.comboBoxTags.currentText()))

    def onColorPicker(self):
        color = QColorDialog.getColor()
        self.widgetColorPreview.setStyleSheet(
            "background-color:" + color.name() + ";")
        self.widgetColorPreview.setObjectName(color.name())

    def populateTags(self):
        for t in self.tags:
            self.comboBoxTags.addItem(t)

    def setPreviewColor(self, tag):
        if tag in self.tags.keys():
            if len(self.tags[tag]) > 0:
                self.widgetColorPreview.setStyleSheet(
                    "background-color: " + self.tags[tag] + ";")
            else:
                self.widgetColorPreview.setStyleSheet(
                    "background-color: rgb(18, 18, 18);")

    def saveTagColor(self):
        inputTag = self.comboBoxTags.currentText()
        newSettings = {}
        for x, y in self.tags.items():
            if x == inputTag:
                newSettings[x] = self.widgetColorPreview.objectName()
        changeLocalData(newSettings, "tags")
        self.accept()


class SettingsDialog(QDialog, Ui_DialogSettings):
    def __init__(self, *args, obj=None, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        readLocalFile("settings")
        self.settings = readLocalFile.data
        self.populateForm()
        
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.saveServerSettings)

    def populateForm(self):
        if self.settings["URL"] != "":
            self.lineEditURL.setText(self.settings["URL"])

        if self.settings["USERNAME"] != "":
            self.lineEditUser.setText(self.settings["USERNAME"])

        if self.settings["PASSWORD"] != "":
            self.lineEditPass.setText(self.settings["PASSWORD"])

    def saveServerSettings(self):
        newSettings = {
            "URL": "",
            "USERNAME": "",
            "PASSWORD": "",
            "CALENDARS": ""
        }
        if self.lineEditURL.text() and self.lineEditUser.text() and self.lineEditPass.text():
            newSettings["URL"] = self.lineEditURL.text()
            newSettings["USERNAME"] = self.lineEditUser.text()
            newSettings["PASSWORD"] = self.lineEditPass.text()
            if "CALENDARS" in self.settings.keys():
                newSettings["CALENDARS"] = self.settings["CALENDARS"]
            
            changeLocalData(newSettings, "settings")
            self.accept()
        else:
            self.warningDialog()
        
    
    def warningDialog(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("DAV Tasks - Warning")
        dlg.setText("All fields must be populated.")
        dlg.exec()

class TaskDialog(QDialog, Ui_EditTaskDialog):
    def __init__(self, uid, *args, obj=None, **kwargs):
        super(TaskDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        readLocalFile("todos")
        self.todos = readLocalFile.data

        readLocalFile("tags")
        self.tags = readLocalFile.data
        
        readLocalFile("settings")
        self.settings = readLocalFile.data
        
        self.populateCalendars()

        saveButton = QPushButton("Save")
        deleteButton = QPushButton("Delete")
        applyButton = QPushButton("Apply")

        if uid == None:
            self.setWindowTitle("DAV Tasks - New Task")
            self.buttonBox.addButton(
                saveButton, self.buttonBox.ButtonRole.YesRole)
            self.populateTags()
            self.comboBoxTags.setCurrentText("")
        else:
            self.setWindowTitle("DAV Tasks - Edit Task")
            self.buttonBox.addButton(
                deleteButton, self.buttonBox.ButtonRole.DestructiveRole)
            self.buttonBox.addButton(
                applyButton, self.buttonBox.ButtonRole.ApplyRole)
            self.populateTags()
            self.populateForm(uid)

        self.checkBoxEnableCalendar.toggled.connect(self.toggleDatePicker)
        saveButton.clicked.connect(lambda: self.submitTodo(None))
        deleteButton.clicked.connect(lambda: self.deleteTodo(uid))
        applyButton.clicked.connect(lambda: self.submitTodo(uid))
        self.buttonBox.rejected.connect(self.reject)

    def deleteTodo(self, uid):
        deleteTodoByUID(uid)
        self.accept()

    def submitTodo(self, uid):

        if not self.comboBoxTags.currentText():
            tag = None
        else:
            tag = self.comboBoxTags.currentText()

        if self.dateEdit.isEnabled():
            createTodo(tag, self.lineEditSummary.text(),
                       self.dateEdit.date(), uid)
        else:
            createTodo(tag, self.lineEditSummary.text(), None, uid)

        self.accept()

    def toggleDatePicker(self):
        if self.dateEdit.isEnabled():
            self.dateEdit.setEnabled(False)
        else:
            self.dateEdit.setEnabled(True)

    def populateForm(self, uid):
        currentDue = None
        keyUID = "UID"

        for t in self.todos.values():
            if keyUID in t.keys():
                if t[keyUID] == uid:

                    if "DUE" in t.keys():
                        currentDueRaw = t["DUE"]
                        currentDue = formatDateNormal(currentDueRaw)

                    if "CATEGORIES" in t.keys():
                        self.comboBoxTags.setCurrentText(t["CATEGORIES"])
                    else:
                        self.comboBoxTags.setCurrentText("")

                    if currentDue == None:
                        self.dateEdit.setDate(date.today())
                        self.dateEdit.setEnabled(False)
                        self.checkBoxEnableCalendar.setChecked(False)
                    else:
                        self.checkBoxEnableCalendar.setChecked(True)
                        self.dateEdit.setEnabled(True)
                        self.dateEdit.setDate(currentDue)

                    self.lineEditSummary.setText(t["SUMMARY"])

    def populateTags(self):

        for t in self.tags:
            self.comboBoxTags.addItem(t)

    def populateCalendars(self):
        for c in self.settings["CALENDARS"]:
            self.comboBoxCalendars.addItem(c)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
