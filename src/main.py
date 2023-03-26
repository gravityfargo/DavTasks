import sys
from datetime import datetime, date
from PyQt6.QtCore import QRect,  Qt, QSize
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFrame, QGridLayout, QWidget, QLabel, QPushButton, QVBoxLayout
import qtawesome as qta
from davconnect import *
from fileutils import sortTodos, readLocalFile, filterByTags
from syncutils import tagCheck, lastFullSyncCheck
from syncWorkers import SyncWorkers
from gui.mainwindow import Ui_MainWindow
from dialogs import EditTagsDialog, settingsDialog, TaskDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # Populate UI
        self.setupUi(self)
        self.setWindowTitle("DAV Tasks")
        self.populateTags()
        self.populateTable("Sort", None, "Due Date", "Ascending")
        
        # UI Template Changes
        syncIcon = qta.icon("fa.refresh")
        settingsIcon = qta.icon("fa.cog")
        buttonIcon = qta.icon("fa.arrow-up")
        self.pushButtonSync.setIcon(syncIcon)
        self.pushButtonSettings.setIcon(settingsIcon)
        self.pushButtonSortOrder.setIcon(buttonIcon)
        self.pushButtonSortOrder.setObjectName("Ascending")
        self.listWidgetTags.setStyleSheet("font-size: 18px;")

        # Button Connections
        self.pushButtonAdd.clicked.connect(self.taskDialog)
        self.pushButtonEditTags.clicked.connect(self.editTagsDialog)
        self.pushButtonSortTags.clicked.connect(lambda: self.sortTasks(self.comboBoxSortTasks.currentText(), self.pushButtonSortOrder.objectName()))
        self.pushButtonSync.clicked.connect(lambda: self.syncDataThread("CalSync", "All", None))
        self.pushButtonSettings.clicked.connect(settingsDialog)
        self.listWidgetTags.itemPressed.connect(lambda: self.filterTag(self.listWidgetTags.currentItem().text()))
        self.pushButtonSortOrder.clicked.connect(self.toggleSortDirectionIcon)        

        # Checks if the app has been synced in the last 4 hours before opening
        if (lastFullSyncCheck()):
            self.syncDataThread("CalSync", "All", None)
            
        tagCheck()

    def syncDataThread(self, task, value1, value2):
        self.pushButtonSync.setEnabled(False)
        self.syncer = SyncWorkers(task, value1, value2)
        self.syncer.setCurrentTask.connect(self.labelProgress.setText)
        self.syncer.finished.connect(self.downloadFinished)
        self.syncer.start()

    def downloadFinished(self):
        self.labelProgress.setText("")
        self.pushButtonSync.setEnabled(True)
        self.clearMainWindow()
        self.refreshGUI()
        del self.syncer

    def populateTable(self, sortOrFilter, filterBy, sortBy, sortDirection):
        # filterBy must be a tag
        # sortBy is a comboBoxSortTasks option
        # sortDirection is asc / dec
        if sortOrFilter == None:
            readLocalFile("todos")
            todos = readLocalFile.data
        elif sortOrFilter == "Filter":
            todos = filterByTags(filterBy)
        elif sortOrFilter == "Sort":
            todos = sortTodos(sortBy, sortDirection)

        readLocalFile("tags")
        tags = readLocalFile.data
        i = 0

        for t in todos.values():

            item = QListWidgetItem(self.listWidgetTasks)

            uid = t["UID"]
            summary = t["SUMMARY"]

            if "DUE" in t.keys():
                rawDate = t["DUE"]
            else:
                rawDate = None

            # Frame
            self.frameTodo = QWidget()
            self.frameTodo.setMaximumHeight(70)
            self.frameTodo.setObjectName(uid)

            # Grid Layout
            self.gridLayoutTodoContent = QGridLayout(self.frameTodo)
            self.gridLayoutTodoContent.setContentsMargins(0, 0, 0, 0)
            self.gridLayoutTodoContent.setVerticalSpacing(0)

            # Frame (to display tag color)
            self.frameTagColor = QFrame()
            self.frameTagColor.setMaximumHeight(70)
            self.frameTagColor.setMaximumWidth(5)
            self.gridLayoutTodoContent.addWidget(self.frameTagColor, 0, 0, 1, 1)

            # Vertical Layout
            self.frameSummary = QFrame()
            self.frameSummary.setMaximumHeight(70)
            self.verticalLayoutSummary = QVBoxLayout(self.frameSummary)
            self.verticalLayoutSummary.setContentsMargins(0,0,0,0)
            self.gridLayoutTodoContent.addWidget(self.frameSummary, 0, 1, 1, 1)
            
            # Tag
            self.labelTag = QLabel()
            self.labelTag.setStyleSheet("color: rgba(255, 255, 255, 0.4);")
            self.verticalLayoutSummary.addWidget(self.labelTag)
            
            # Summary
            self.labelSummary = QLabel()
            self.labelSummary.setText(summary)
            self.labelSummary.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: bold; font-size: 18px;")
            self.labelSummary.setWordWrap(True)
            self.verticalLayoutSummary.addWidget(self.labelSummary)
            self.verticalLayoutSummary.addStretch()
            
            # Set the tag color frame
            if "CATEGORIES" in t:
                tag = t["CATEGORIES"]
                self.labelTag.setText(tag)
                if tag in tags.keys() and len(tags[tag]) > 0:
                    self.frameTagColor.setStyleSheet(
                        "background-color: " + tags[tag] + ";")

            # Frame
            self.frameDuedays = QFrame()
            self.frameDuedays.setStyleSheet("background-color: rgba(0,0,0,0.05);")
            self.frameDuedays.setMaximumWidth(80)
            self.gridLayoutTodoContent.addWidget(self.frameDuedays, 0, 2, 1, 1)
            
            # Vertical Layout
            self.verticalLayoutDueDays = QVBoxLayout(self.frameDuedays)
            self.verticalLayoutDueDays.setContentsMargins(0,0,0,0)
            
            # Due days
            self.labelCountdown = QLabel()
            self.verticalLayoutDueDays.addWidget(self.labelCountdown)
            self.labelCountdown.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

            # Frame
            self.frameDate = QFrame()
            self.gridLayoutTodoContent.addWidget(self.frameDate, 0, 3, 1, 1)
            self.frameDate.setMaximumWidth(80)
            self.gridLayoutDate = QGridLayout(self.frameDate)
            
            if rawDate != None:
                today = date.today()
                formattedDate = datetime.strptime(rawDate, '%Y-%m-%d %H:%M:%S')
                delta = formattedDate.date() - today
                self.labelCountdown.setText(str(delta.days))
                if delta.days == 0:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(204,51,0);")
                if delta.days == 1:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(255,153,102);")
                if delta.days == 2:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(255,204,0);")
                if delta.days == 3:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(153,204,51);")
                if delta.days > 3 and delta.days <= 30:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(51, 153, 0);")
                if delta.days > 30:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(51, 153, 0);")
                    self.labelCountdown.setText("30+")
                if delta.days < 0:
                    self.labelCountdown.setStyleSheet(
                        "color: rgb(204, 51, 0);")
                    self.labelCountdown.setText("Overdue")

                # Day
                self.labelDateDay = QLabel()
                formattedDayofWeek = datetime.strftime(formattedDate, '%a')
                self.labelDateDay.setText(formattedDayofWeek)
                self.labelDateDay.setStyleSheet("color: rgba(255, 255, 255, 0.5);")
                self.labelDateDay.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.gridLayoutDate.addWidget(self.labelDateDay, 0, 0, 1, 1)

                # Date
                self.labelDate = QLabel()
                self.labelDate.setText(str(formattedDate.month) + "-" + str(formattedDate.day))
                self.labelDate.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.labelDate.setStyleSheet("border-top: 2px solid rgba(0,0,0,0.2); padding-top: 6;")
                self.gridLayoutDate.addWidget(self.labelDate, 1, 0, 1, 1)

            # Frame
            self.frameButtons = QFrame()
            self.frameButtons.setMaximumWidth(40)
            self.verticalLayoutButtons = QVBoxLayout(self.frameButtons)
            self.verticalLayoutButtons.setSpacing(0)
            self.gridLayoutTodoContent.addWidget(self.frameButtons, 0, 4, 1, 1)

            # Edit Button
            self.pushButtonEdit = QPushButton()
            self.pushButtonEdit.clicked.connect(self.taskDialog)
            self.pushButtonEdit.setObjectName("pushButtonEdit_" + uid)
            pushButtonEditIcon = qta.icon("fa5.edit", color=("White", 50), offset=(0.1,0))
            self.pushButtonEdit.setIcon(QIcon(pushButtonEditIcon))
            self.pushButtonEdit.setFlat(True)
            self.verticalLayoutButtons.addWidget(self.pushButtonEdit)

            # Complete Button
            self.pushButtonComplete = QPushButton()
            self.pushButtonComplete.clicked.connect(self.completeTask)
            self.pushButtonComplete.setObjectName("pushButtonCompleted_" + uid)
            pushButtonCompleteIcon = qta.icon("fa5.check-circle", color=("White", 50))
            self.pushButtonComplete.setIcon(QIcon(pushButtonCompleteIcon))
            self.pushButtonComplete.setFlat(True)
            self.verticalLayoutButtons.addWidget(self.pushButtonComplete)

            item.setSizeHint(QSize(0, 70))
            self.listWidgetTasks.addItem(item)
            self.listWidgetTasks.setItemWidget(item, self.frameTodo)

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        itemTag = QListWidgetItem()
        itemTag.setText("All Tags")
        self.listWidgetTags.addItem(itemTag)
        for t in tags:
            itemTag = QListWidgetItem()
            itemTag.setText(t)

            if len(tags[t]) != 0:
                itemTag.setForeground(QColor().black())
                itemTag.setBackground(QColor(tags[t]))
            self.listWidgetTags.addItem(itemTag)
        self.listWidgetTags.sortItems(Qt.SortOrder.AscendingOrder)

    def clearMainWindow(self):
        self.listWidgetTags.clear()
        self.listWidgetTasks.clear()

    def refreshGUI(self):
        self.clearMainWindow()
        self.populateTags()
        self.populateTable("Sort", None, "Due Date", "Ascending")
        # I really shouldnt do this here
        tagCheck()

    def sortTasks(self, byWhat, direction):
        self.clearMainWindow()
        self.populateTags()
        self.populateTable("Sort", None, byWhat, direction)

    def toggleSortDirectionIcon(self):
        if (self.pushButtonSortOrder.objectName() == "Ascending"):
            buttonIcon = qta.icon("fa.arrow-down")
            self.pushButtonSortOrder.setIcon(buttonIcon)
            self.pushButtonSortOrder.setObjectName("Descending")
        else:
            buttonIcon = qta.icon("fa.arrow-up")
            self.pushButtonSortOrder.setIcon(buttonIcon)
            self.pushButtonSortOrder.setObjectName("Ascending")


    def filterTag(self, tag):
        self.clearMainWindow()
        self.populateTags()
        if tag == "All Tags":
            self.populateTable(None, None, None, None)
        else:
            self.populateTable("Filter", tag, None, None)

    def completeTask(self):
        uid = self.sender().objectName()[20:]
        self.syncDataThread("CompleteTask", uid, None)

    def editTagsDialog(self):
        dlg = EditTagsDialog()
        if dlg.exec():
            self.refreshGUI()

    def taskDialog(self):
        if self.sender().objectName() == "pushButtonAdd":
            dlg = TaskDialog(None)
        else:
            uid = self.sender().objectName()[15:]
            dlg = TaskDialog(uid)

        dlg.exec()
        if (dlg.task == "CreateTask"):
            self.syncDataThread(
                "CreateTask", dlg.newTaskDict, dlg.newTaskCalendar)
            
        elif (dlg.task == "ModifyTask"):
            self.syncDataThread("ModifyTask", dlg.moddedTask,
                                dlg.moddedTaskCalendar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
