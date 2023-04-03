from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from fileutils import *
from davconnect import *
from icalendar.prop import vCategory, vDatetime
import uuid
from syncutils import tagCheck
import time


class SyncWorkers(QThread):

    setTotalProgress = pyqtSignal(int)
    setCurrentProgress = pyqtSignal(int)
    setCurrentTask = pyqtSignal(str)
    succeeded = pyqtSignal()

    def __init__(self, task, value1, value2):
        super().__init__()

        self.value1 = value1
        self.value2 = value2
        self.task = task

        # Task:     CalSync
        # Value1:   whichCalendar
        #               - all
        #               - <AnyCalendar>

        # Task:     completeTask
        # Value1:
        # Value2:   UID

        # Task:     TaskModify
        # Value1:   taskDict
        # Value2:   UID

        # Task:     CreateTask
        # Value1:   taskDict
        # Value2:   calendar

    def run(self):
        if (self.task == "CalSync"):
            if (self.value1 == "All"):
                self.syncCalendars("All")
                self.setCurrentTask.emit("Syncing All Calendars")

        if (self.task == "CompleteTask"):
            self.markTaskCompleteUpstream(self.value1)
            self.setCurrentTask.emit("Marking task complete.")

        if (self.task == "CreateTask"):
            self.createTodo(self.value1, self.value2)
            self.setCurrentTask.emit("Creating Task")

        if (self.task == "ModifyTask"):
            self.modifyTask(self.value1, self.value2)
            self.setCurrentTask.emit("Modifying Task.")

    def modifyTask(self, taskToModify, cal):
        readLocalFile("todos")
        tasks = readLocalFile.data
        modifiedTasks = tasks.copy()
        curretTask = tasks[taskToModify["UID"]]

        serverConnect()
        calendar = serverConnect.my_principal.calendar(cal)

        taskFetched = calendar.search(
            todo=True,
            uid=taskToModify["UID"],
        )
        if not taskFetched:
            print("Didn't find it.")
        else:
            task = taskFetched[0]
            task.icalendar_component["summary"] = task.icalendar_component["summary"].replace(
                curretTask["SUMMARY"], taskToModify["SUMMARY"])

            if "DUE" in taskToModify.keys():
                nDS = datetime.strptime(
                    taskToModify["DUE"], "%Y-%m-%d %H:%M:%S")
                formattedDate = vDatetime(nDS).to_ical()
                task.icalendar_component["DTSTART"] = formattedDate
                task.icalendar_component["DUE"] = formattedDate

            if "CATEGORIES" in taskToModify.keys():
                newCatList = []
                newCatList.append(taskToModify["CATEGORIES"])
                newCat = vCategory(newCatList).to_ical()
                task.icalendar_component["CATEGORIES"] = newCat

            # Update the time modified in localjson so local data is up to date.
            localTask = modifiedTasks[taskToModify["UID"]]
            if "LAST-MODIFIED" in localTask.keys():
                nDS = datetime.now()
                formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
                localTask["LAST-MODIFIED"] = formattedDate

            task.save()

            changeLocalData(None, "todos")
            changeLocalData(modifiedTasks, "todos")
            self.syncCalendars(cal)

    def syncCalendars(self, whichCalendar):

        readLocalFile("settings")
        settings = readLocalFile.data
        newSettings = settings.copy()

        readLocalFile("tags")
        tags = readLocalFile.data
        modifiedTags = tags.copy()

        readLocalFile("todos")
        tasks = readLocalFile.data
        modifiedTasks = tasks.copy()

        readLocalFile("completedTodos")
        completedTasks = readLocalFile.data
        modifiedcompletedTasks = completedTasks.copy()
        keys = tasks.keys()

        calendarsToSync = []
        upstreamTagUidList = []

        if whichCalendar == "All":
            self.setCurrentTask.emit("Starting a full sync.")
            time.sleep(1)
            for c in settings["ENABLEDCALENDARS"]:
                calendarsToSync.append(str(c))

            # Adds a timestamp in json indicating when the last full calendar sync was.
            nDS = datetime.now()
            formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
            newSettings["LASTSYNC"] = formattedDate

        else:
            calendarsToSync.append(whichCalendar)

        for calendar in calendarsToSync:
            self.setCurrentTask.emit("Syncing Calendar " + calendar)
            serverConnect()
            calendar = serverConnect.my_principal.calendar(calendar)
            todos = calendar.todos()

            for t in todos:
                upstreamTask = t.icalendar_component
                upstreamUID = upstreamTask["UID"].to_ical().decode()

                if upstreamUID in keys:
                    upstreamTagUidList.append(upstreamUID)
                    if "LAST-MODIFIED" in upstreamTask.keys():
                        upstreamLastMod = str(upstreamTask["LAST-MODIFIED"].dt)
                    elif "LAST-MODIFIED" not in upstreamTask.keys():
                        nDS = datetime.now()
                        formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
                        upstreamLastMod = formattedDate

                    localTask = modifiedTasks[upstreamUID]
                    if "LAST-MODIFIED" not in localTask.keys():
                        nDS = datetime.now()
                        formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
                        localTask["LAST-MODIFIED"] = formattedDate

                    if upstreamLastMod != localTask["LAST-MODIFIED"]:
                        for keyToUpdate in upstreamTask.keys():
                            if keyToUpdate == "LAST-MODIFIED" or keyToUpdate == "CREATED" or keyToUpdate == "DTSTAMP" or keyToUpdate == "DTSTART":
                                localTask[keyToUpdate] = str(
                                    upstreamTask[keyToUpdate].dt)
                            elif keyToUpdate == "DUE":
                                nDS = upstreamTask[keyToUpdate].dt
                                localTask[keyToUpdate] = nDS.strftime(
                                    "%Y-%m-%d %H:%M:%S")
                            elif keyToUpdate == "CATEGORIES":
                                cat = upstreamTask[keyToUpdate].to_ical(
                                ).decode()
                                localTask[keyToUpdate] = cat
                                if cat not in modifiedTags.keys():
                                    modifiedTags[cat] = {}
                            else:
                                localTask[keyToUpdate] = upstreamTask[keyToUpdate]

                        localTask["INCALENDAR"] = str(calendar)
                        modifiedTasks[upstreamUID] = localTask

                elif upstreamUID not in keys:
                    upstreamTagUidList.append(upstreamUID)
                    newTask = {}
                    for keyToCreate in upstreamTask.keys():

                        if keyToCreate == "LAST-MODIFIED" or keyToCreate == "CREATED" or keyToCreate == "DTSTAMP" or keyToCreate == "DTSTART":
                            newTask[keyToCreate] = str(
                                upstreamTask[keyToCreate].dt)
                        elif keyToCreate == "DUE":
                            nDS = upstreamTask[keyToCreate].dt
                            newTask[keyToCreate] = nDS.strftime(
                                "%Y-%m-%d %H:%M:%S")
                        elif keyToCreate == "CATEGORIES":
                            cat = upstreamTask[keyToCreate].to_ical().decode()
                            newTask[keyToCreate] = cat
                            if cat not in modifiedTags.keys():
                                modifiedTags[cat] = {}
                        else:
                            newTask[keyToCreate] = upstreamTask[keyToCreate]

                    if "LAST-MODIFIED" not in newTask.keys():
                        nDS = datetime.now()
                        formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
                        newTask["LAST-MODIFIED"] = formattedDate

                    newTask["INCALENDAR"] = str(calendar)
                    modifiedTasks[upstreamUID] = newTask

            # moves tasks marked completed upstream into the completedtasks dict
            # if the task exists locally, but was deleted upstream, this deletes them locally. (only for the current calendar in the for loop)
            for uid, details in tasks.items():

                if details["INCALENDAR"] == str(calendar):

                    if uid not in upstreamTagUidList and len(upstreamTagUidList) > 0:
                        taskFetched = calendar.search(
                            todo=True,
                            include_completed=True,
                            uid=uid,
                        )
                        if taskFetched:
                            completedUID = taskFetched[0].icalendar_component["UID"]
                            if completedUID not in modifiedcompletedTasks.keys():
                                modifiedcompletedTasks[completedUID] = tasks[completedUID]
                            del modifiedTasks[completedUID]
                        else:
                            del modifiedTasks[uid]

            upstreamTagUidList.clear()

        # This checks all of the tasks in json if they are in a calendar that is currently enabled. If the calendar isn't enabled, it deletes the task.
        for uid, details in tasks.items():
            if details["INCALENDAR"] not in calendarsToSync:
                del modifiedTasks[uid]

        changeLocalData(newSettings, "settings")
        changeLocalData(None, "completedTodos")
        changeLocalData(modifiedcompletedTasks, "completedTodos")
        changeLocalData(None, "todos")
        changeLocalData(modifiedTasks, "todos")
        tagCheck()
        self.setCurrentTask.emit("Sync Complete.")
        time.sleep(1)
        self.succeeded.emit()

    def markTaskCompleteUpstream(self, uid):

        self.setTotalProgress.emit(2)
        self.setCurrentTask.emit("Marking task as complete...")

        readLocalFile("todos")
        todos = readLocalFile.data
        modifiedTodos = todos.copy()
        curretTask = todos[uid]

        readLocalFile("completedTodos")
        completedTodos = readLocalFile.data
        modifiedCompletedTodos = completedTodos.copy()

        serverConnect()
        calendar = serverConnect.my_principal.calendar(
            curretTask["INCALENDAR"])

        taskFetched = calendar.search(
            todo=True,
            uid=uid
        )
        if not taskFetched:
            self.setCurrentTask.emit("Task not on server.")
        else:
            task = taskFetched[0]

            self.setCurrentProgress.emit(1)
            self.setCurrentTask.emit("Task found.")
            modifiedCompletedTodos[uid] = curretTask
            del modifiedTodos[uid]
            task.complete()
            task.save()

            # serverSync(task["INCALENDAR"])
            changeLocalData(None, "todos")
            changeLocalData(modifiedTodos, "todos")
            changeLocalData(None, "completedTodos")
            changeLocalData(modifiedCompletedTodos, "completedTodos")
            self.setCurrentTask.emit("Task marked completed")

    # Creates a new todo from a dictionary and adds it to local json and creates the task on the server.
    def createTodo(self, taskDict, cal):
        readLocalFile("todos")
        tasks = readLocalFile.data
        modifiedTasks = tasks.copy()

        self.setCurrentTask.emit("Creating Task")

        serverConnect()
        calendar = serverConnect.my_principal.calendar(cal)
        assert len(taskDict) > 0

        uidNew = uuid.uuid4()

        if "LAST-MODIFIED" not in taskDict.keys():
            nDS = datetime.now()
            formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
            taskDict["LAST-MODIFIED"] = formattedDate

        if "DUE" in taskDict.keys():
            nDS = datetime.strptime(taskDict["DUE"], "%Y-%m-%d %H:%M:%S")
            formattedDate = nDS.date()

        if "CATEGORIES" in taskDict.keys() and "DUE" in taskDict.keys():
            calendar.save_todo(
                summary=taskDict["SUMMARY"],
                due=formattedDate,
                categories=[taskDict["CATEGORIES"]],
                uid=uidNew
            )

        elif "CATEGORIES" in taskDict.keys() and "DUE" not in taskDict.keys():
            calendar.save_todo(
                summary=taskDict["SUMMARY"],
                categories=[taskDict["CATEGORIES"]],
                uid=uidNew
            )

        elif "CATEGORIES" not in taskDict.keys() and "DUE" in taskDict.keys():
            calendar.save_todo(
                summary=taskDict["SUMMARY"],
                due=formattedDate,
                uid=uidNew
            )
        else:
            calendar.save_todo(
                summary=taskDict["SUMMARY"],
                uid=uidNew
            )
        taskDict["INCALENDAR"] = cal
        taskDict["UID"] = str(uidNew)
        modifiedTasks[str(uidNew)] = taskDict

        changeLocalData(None, "todos")
        changeLocalData(modifiedTasks, "todos")
