import sys
from datetime import datetime, date
from PyQt6.QtCore import QRect,  Qt, QSize
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFrame, QGridLayout, QWidget, QLabel, QPushButton
import qtawesome as qta
from davconnect import *
from fileutils import sortTodos, readLocalFile, filterByTags
from syncutils import tagCheck
from syncWorkers import SyncWorkers
from gui.mainwindow import Ui_MainWindow
from dialogs import EditTagsDialog, settingsDialog, TaskDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("DAV Tasks")

        self.populateTags()
        self.populateTable("Sort", None, "Due Date", "Ascending")

        self.pushButtonAdd.clicked.connect(self.taskDialog)
        self.pushButtonEditTags.clicked.connect(self.editTagsDialog)
        self.pushButtonSortTags.clicked.connect(lambda: self.sortTasks(
            self.comboBoxSortTasks.currentText(), self.comboBoxSortDirection.currentText()))

        self.pushButtonSync.clicked.connect(
            lambda: self.syncDataThread("CalSync", "All", None))
        self.pushButtonSettings.clicked.connect(settingsDialog)
        self.listWidgetTags.itemPressed.connect(
            lambda: self.filterTag(self.listWidgetTags.currentItem().text()))

        syncIcon = qta.icon("fa.refresh")
        self.pushButtonSync.setIcon(syncIcon)

    def syncDataThread(self, task, value1, value2):
        self.pushButtonSync.setEnabled(False)
        self.syncer = SyncWorkers(task, value1, value2)
        self.syncer.setCurrentTask.connect(self.labelProgress.setText)
        self.syncer.finished.connect(self.downloadFinished)
        self.syncer.start()

    def downloadFinished(self):
        print("Finished")
        self.progressBar.setValue(self.progressBar.minimum())
        self.labelProgress.setText("")
        self.pushButtonSync.setEnabled(True)
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

            self.frameTodo = QWidget()
            self.frameTodo.setGeometry(QRect(0, 0, 16777215, 60))

            self.frameTodo.setObjectName(uid)

            self.gridLayoutTodo = QGridLayout(self.frameTodo)
            self.gridLayoutTodo.setContentsMargins(0, 0, 0, 0)

            self.frameTag = QFrame()
            self.gridLayoutTodo.addWidget(self.frameTag, 0, 0, 1, 1)

            self.gridLayoutTag = QGridLayout(self.frameTag)
            self.gridLayoutTag.setContentsMargins(0, 0, 0, 0)

            self.frameTagColor = QFrame()
            self.frameTagColor.setFixedSize(QSize(15, 60))
            self.gridLayoutTag.addWidget(self.frameTagColor, 0, 0, 1, 1)

            self.labelTag = QLabel()
            self.labelTag.setStyleSheet("color: rgb(120, 120, 120);")
            self.gridLayoutTag.addWidget(self.labelTag, 0, 1, 1, 1)

            if "CATEGORIES" in t:
                tag = t["CATEGORIES"]
                self.labelTag.setText(tag)
                if tag in tags.keys() and len(tags[tag]) > 0:
                    self.frameTagColor.setStyleSheet(
                        "background-color: " + tags[tag] + ";")

            self.frameSummary = QFrame()
            self.gridLayoutSummary = QGridLayout(self.frameSummary)
            self.gridLayoutSummary.setSpacing(0)
            self.gridLayoutTodo.addWidget(self.frameSummary, 0, 1, 1, 1)

            self.labelSummary = QLabel()
            self.labelSummary.setText(summary)
            self.labelSummary.setWordWrap(True)
            self.labelSummary.setStyleSheet("font: 13pt \"Arial\";")
            self.labelSummary.setContentsMargins(0, 0, 0, 0)
            self.labelSummary.setAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            self.gridLayoutSummary.addWidget(self.labelSummary, 0, 0, 1, 1)

            self.frameDuedays = QFrame()
            self.gridLayoutTodo.addWidget(self.frameDuedays, 0, 2, 1, 1)

            self.gridLayoutCountdown = QGridLayout(self.frameDuedays)
            self.gridLayoutCountdown.setContentsMargins(0, 0, 0, 0)

            self.labelCountdown = QLabel()
            font = QFont()
            font.setBold(True)
            self.labelCountdown.setFont(font)
            self.labelCountdown.setStyleSheet(
                "color: rgb(0, 0, 0); font: 12pt;")
            self.gridLayoutCountdown.addWidget(self.labelCountdown, 0, 0, 1, 1)
            self.labelCountdown.setAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

            self.frameDate = QFrame()
            self.gridLayoutTodo.addWidget(self.frameDate, 0, 3, 1, 1)
            self.gridLayoutDate = QGridLayout(self.frameDate)

            self.pushButtonEdit = QPushButton()
            self.pushButtonEdit.clicked.connect(self.taskDialog)
            self.pushButtonEdit.setObjectName("pushButtonEdit_" + uid)
            self.pushButtonEdit.setFixedSize(QSize(30, 60))
            pushButtonEditIcon = qta.icon("fa5.edit")
            self.pushButtonEdit.setIcon(QIcon(pushButtonEditIcon))
            self.pushButtonEdit.setFlat(True)
            self.gridLayoutTodo.addWidget(self.pushButtonEdit, 0, 4, 1, 1)

            self.pushButtonComplete = QPushButton()
            self.pushButtonComplete.clicked.connect(self.completeTask)
            self.pushButtonComplete.setObjectName("pushButtonCompleted_" + uid)
            self.pushButtonComplete.setFixedSize(QSize(30, 60))
            pushButtonCompleteIcon = qta.icon("fa5.check-circle")
            self.pushButtonComplete.setIcon(QIcon(pushButtonCompleteIcon))
            self.pushButtonComplete.setFlat(True)
            self.gridLayoutTodo.addWidget(self.pushButtonComplete, 0, 5, 1, 1)

            self.gridLayoutTodo.setColumnStretch(0, 1)
            self.gridLayoutTodo.setColumnStretch(1, 6)
            self.gridLayoutTodo.setColumnStretch(2, 1)
            self.gridLayoutTodo.setColumnStretch(3, 1)
            self.gridLayoutTodo.setColumnStretch(4, 1)
            self.gridLayoutTodo.setColumnStretch(5, 1)

            if rawDate == None:
                self.labelCountdown.setStyleSheet("color: rgb(51, 51, 51);")

            else:
                today = date.today()
                # 2023-02-04 17:00:00
                formattedDate = datetime.strptime(rawDate, '%Y-%m-%d %H:%M:%S')
                delta = formattedDate.date() - today
                self.labelCountdown.setText(str(delta.days))
                if delta.days == 0:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(204,51,0);")
                if delta.days == 1:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(255,153,102);")
                if delta.days == 2:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(255,204,0);")
                if delta.days == 3:
                    self.frameDuedays.setStyleSheet(
                        "background-color: rgb(153,204,51);")
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

                self.labelDateDay = QLabel()
                formattedDayofWeek = datetime.strftime(formattedDate, '%a')
                self.labelDateDay.setText(formattedDayofWeek)
                self.labelDateDay.setAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.labelDateDay.setStyleSheet("color: rgb(120, 120, 120);")
                self.gridLayoutDate.addWidget(self.labelDateDay, 0, 0, 1, 1)

                self.labelDate = QLabel()
                self.labelDate.setText(
                    str(formattedDate.month) + "-" + str(formattedDate.day))
                self.labelDate.setAlignment(
                    Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.gridLayoutDate.addWidget(self.labelDate, 1, 0, 1, 1)

            item.setSizeHint(QSize(0, 60))
            self.listWidgetTasks.addItem(item)
            self.listWidgetTasks.setItemWidget(item, self.frameTodo)

    def populateTags(self):
        readLocalFile("tags")
        tags = readLocalFile.data
        item = QListWidgetItem()
        item.setText("All Tags")
        self.listWidgetTags.addItem(item)
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
            print("Making Task exec")

        elif (dlg.task == "ModifyTask"):
            self.syncDataThread("ModifyTask", dlg.moddedTask,
                                dlg.moddedTaskCalendar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
