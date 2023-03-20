from PyQt6.QtWidgets import QMessageBox, QColorDialog, QPushButton, QDialog
from gui.settingsdialog import Ui_DialogSettings
from gui.edittags import *
from gui.edittask import *
from gui.multipurposeDialog import *
from fileutils import *
from davconnect import *



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
            getCalendars()
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

        self.newTaskDict = {}
        self.newTaskCalendar = ""
        self.task = ""
        
        self.moddedTask = {}
        self.moddedTaskCalendar = ""

        saveButton = QPushButton("Save")
        # deleteButton = QPushButton("Delete")
        applyButton = QPushButton("Apply")

        self.dateEdit.setDate(date.today())

        if uid == None:
            self.setWindowTitle("DAV Tasks - New Task")
            self.buttonBox.addButton(
                saveButton, self.buttonBox.ButtonRole.YesRole)
            self.populateTags()
            self.comboBoxTags.setCurrentText("")
        else:
            self.setWindowTitle("DAV Tasks - Edit Task")
            # self.buttonBox.addButton(
                # deleteButton, self.buttonBox.ButtonRole.DestructiveRole)
            self.buttonBox.addButton(
                applyButton, self.buttonBox.ButtonRole.ApplyRole)
            self.populateTags()
            self.populateForm(uid)

        self.checkBoxEnableCalendar.toggled.connect(self.toggleDatePicker)
        saveButton.clicked.connect(self.newTask)
        # deleteButton.clicked.connect(lambda: self.completeTodo(uid))
        applyButton.clicked.connect(lambda: self.modifyTask(uid))
        self.buttonBox.rejected.connect(self.reject)

    def modifyTask(self, uid):
        self.moddedTaskCalendar = self.comboBoxCalendars.currentText()
        self.moddedTask = {
            "SUMMARY": self.lineEditSummary.text(),
            "UID": uid
        }

        if self.comboBoxTags.currentText():
            self.moddedTask['CATEGORIES'] = self.comboBoxTags.currentText()

        if self.dateEdit.isEnabled():
            nDS = self.dateEdit.date().toPyDate()
            formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
            self.moddedTask["DUE"] = formattedDate

        self.task = "ModifyTask"
        self.accept()

    def newTask(self):

        self.newTaskCalendar = self.comboBoxCalendars.currentText()
        self.newTaskDict = {
            "SUMMARY": self.lineEditSummary.text()
        }

        if self.comboBoxTags.currentText():
            self.newTaskDict['CATEGORIES'] = self.comboBoxTags.currentText()

        if self.dateEdit.isEnabled():
            nDS = self.dateEdit.date().toPyDate()
            formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
            self.newTaskDict["DUE"] = formattedDate

        self.task = "CreateTask"

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
                        currentDue = datetime.strptime(
                            currentDueRaw, '%Y-%m-%d %H:%M:%S')

                    if "CATEGORIES" in t.keys():
                        self.comboBoxTags.setCurrentText(t["CATEGORIES"])
                    else:
                        self.comboBoxTags.setCurrentText("")

                    if currentDue == None:
                        self.dateEdit.setEnabled(False)
                        self.checkBoxEnableCalendar.setChecked(False)
                    else:
                        self.checkBoxEnableCalendar.setChecked(True)
                        self.dateEdit.setEnabled(True)
                        self.dateEdit.setDate(currentDue)

                    self.comboBoxCalendars.setCurrentText(t["INCALENDAR"])
                    self.lineEditSummary.setText(t["SUMMARY"])

    def populateTags(self):
        for t in self.tags:
            self.comboBoxTags.addItem(t)

    def populateCalendars(self):
        for c in self.settings["CALENDARS"]:
            self.comboBoxCalendars.addItem(c)
        self.accept()

class MultipurposeDialog(QDialog, Ui_MultipurposeDialog):
    def __init__(self, title, description, *args, obj=None, **kwargs):
        super(MultipurposeDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
