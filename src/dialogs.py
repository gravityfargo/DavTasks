from PyQt6.QtWidgets import QCheckBox, QColorDialog, QLineEdit, QPushButton, QDialog, QDialogButtonBox, QFrame, QGridLayout, QFormLayout
from PyQt6.QtCore import QSize
from gui.settingsdialog import Ui_DialogSettings
from gui.edittags import Ui_EditTagDialog
from gui.edittask import Ui_EditTaskDialog
from gui.multipurposeDialog import Ui_MultipurposeDialog
from fileutils import readLocalFile, changeLocalData
from davconnect import getCalendars
import traceback
from datetime import date, datetime


class EditTagsDialog(QDialog, Ui_EditTagDialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(EditTagsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        readLocalFile("tags")
        self.tags = readLocalFile.data
        self.modifiedTags = self.tags.copy()
        
        readLocalFile("oldTags")
        self.oldTags = readLocalFile.data
        self.modifiedOldTags = self.tags.copy()
        
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
        for tag, y in self.tags.items():
            if tag == inputTag:
                self.modifiedTags[tag] = self.widgetColorPreview.objectName()
                self.modifiedOldTags[tag] = self.widgetColorPreview.objectName()
        changeLocalData(None, "tags")
        changeLocalData(self.modifiedTags, "tags")
        changeLocalData(None, "oldTags")
        changeLocalData(self.modifiedOldTags, "oldTags")
        self.accept()


def settingsDialog():
    dlg = SettingsDialog()
    dlg.exec()


class SettingsDialog(QDialog, Ui_DialogSettings):
    def __init__(self, *args, obj=None, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        readLocalFile("settings")
        self.settings = readLocalFile.data
        self.populateExistingSettings()

        self.saveButton = self.buttonBox.button(QDialogButtonBox.Save)
        self.resetButton = self.buttonBox.button(QDialogButtonBox.Reset)

        if (self.settings["CALENDARS"]):
            self.pushButtonConnect.setEnabled(False)
            self.populateCalendars()
        else:
            self.buttonBox.removeButton(self.saveButton)
            self.buttonBox.removeButton(self.resetButton)
            self.comboBoxCalendars.setEnabled(False)

        self.pushButtonConnect.clicked.connect(self.saveServerSettings)
        self.resetButton.clicked.connect(self.clearForms)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.saveCalendarSettings)

    def populateExistingSettings(self):
        if self.settings["URL"] != "":
            self.lineEditURL.setText(self.settings["URL"])

        if self.settings["USERNAME"] != "":
            self.lineEditUser.setText(self.settings["USERNAME"])

        if self.settings["PASSWORD"] != "":
            self.lineEditPass.setText(self.settings["PASSWORD"])

    def populateCalendars(self):
        readLocalFile("settings")
        settings = readLocalFile.data

        defaultCal = self.settings["DEFAULTCAL"]
        self.comboBoxCalendars.addItem(defaultCal)

        i = 0
        for c in settings["CALENDARS"]:
            if (c != defaultCal):
                self.comboBoxCalendars.addItem(c)
            self.checkBox = QCheckBox(parent=self.gridWidget)
            self.checkBox.setText(c)
            self.gridLayoutCheckBoxes.addWidget(self.checkBox, i, 0, 1, 1)
            if (c in settings["ENABLEDCALENDARS"]):
                self.checkBox.setChecked(True)
            i = i + 1

    def saveServerSettings(self):
        newSettings = {
            "URL": "",
            "USERNAME": "",
            "PASSWORD": "",
            "CALENDARS": "",
            "DEFAULTCAL": ""
        }
        if self.lineEditURL.text() and self.lineEditUser.text() and self.lineEditPass.text():
            newSettings["URL"] = self.lineEditURL.text()
            newSettings["USERNAME"] = self.lineEditUser.text()
            newSettings["PASSWORD"] = self.lineEditPass.text()
            newSettings["CALENDARS"] = self.settings["CALENDARS"]
            changeLocalData(newSettings, "settings")

            try:
                getCalendars()
                self.comboBoxCalendars.setEnabled(True)
                self.buttonBox.addButton(QDialogButtonBox.Save)
                self.populateCalendars()
            except Exception as a:
                # need to fix this
                multipurposeDialog(str(a))

        else:
            multipurposeDialog("All fields must be populated.")

    def saveCalendarSettings(self):
        calendarsSelected = {
        }

        finalDict = {
            "ENABLEDCALENDARS": calendarsSelected,
            "DEFAULTCAL": self.comboBoxCalendars.currentText()
        }
        readLocalFile("settings")
        settings = readLocalFile.data
        allCalendars = settings["CALENDARS"]

        for widgetchild in self.gridWidget.children():
            if isinstance(widgetchild, QCheckBox):
                if (widgetchild.isChecked() == True):
                    calendarsSelected[widgetchild.text(
                    )] = allCalendars[widgetchild.text()]

        changeLocalData(finalDict, "settings")
        self.accept()

    def clearForms(self):
        self.buttonBox.removeButton(self.saveButton)
        self.buttonBox.removeButton(self.resetButton)
        self.comboBoxCalendars.setEnabled(False)
        self.comboBoxCalendars.clear()
        self.pushButtonConnect.setEnabled(True)
        self.lineEditUser.clear()
        self.lineEditPass.clear()
        self.lineEditURL.clear()
        newSettings = {
            "URL": "",
            "USERNAME": "",
            "PASSWORD": "",
            "CALENDARS": "",
            "DEFAULTCAL": ""
        }
        childWidgets = self.gridWidget.findChildren(QCheckBox)
        for child in childWidgets:
            self.gridLayoutCheckBoxes.removeWidget(child)
        changeLocalData(newSettings, "settings")

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
        defaultCal = self.settings["DEFAULTCAL"]
        self.comboBoxCalendars.addItem(defaultCal)
        for c in self.settings["ENABLEDCALENDARS"]:
            if (c != defaultCal):
                self.comboBoxCalendars.addItem(c)
        self.accept()


def multipurposeDialog(description):
    dlg = MultipurposeDialog(description)
    dlg.exec()


class MultipurposeDialog(QDialog, Ui_MultipurposeDialog):
    def __init__(self, description, *args, obj=None, **kwargs):
        super(MultipurposeDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.descriptionLabel.setText(description)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
