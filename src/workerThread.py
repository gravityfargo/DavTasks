import sys, traceback
import time
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from fileutils import *
from davconnect import *
from icalendar.prop import vCategory, vDatetime
import uuid

class SyncWorker(QThread):

    # Signal for the window to establish the maximum value
    # # of the progress bar.
    setTotalProgress = pyqtSignal(int)
    # # Signal to increase the progress.
    setCurrentProgress = pyqtSignal(int)

    setCurrentTask = pyqtSignal(str)
    # # Signal to be emitted when the file has been downloaded successfully.
    succeeded = pyqtSignal()

    def __init__(self, whichCalendar):
        super().__init__()

        self.whichCalendar = whichCalendar

    # def run(self):
    #     print("Test")
        # url = "https://www.python.org/ftp/python/3.7.2/python-3.7.2.exe"
        # filename = "python-3.7.2.exe"
        # readBytes = 0
        # chunkSize = 1024
        # # Open the URL address.
        # with urlopen(url) as r:
        #     # Tell the window the amount of bytes to be downloaded.
        #     self.setTotalProgress.emit(int(r.info()["Content-Length"]))
        #     with open(filename, "ab") as f:
        #         while True:
        #             # Read a piece of the file we are downloading.
        #             chunk = r.read(chunkSize)
        #             # If the result is `None`, that means data is not
        #             # downloaded yet. Just keep waiting.
        #             if chunk is None:
        #                 continue
        #             # If the result is an empty `bytes` instance, then
        #             # the file is complete.
        #             elif chunk == b"":
        #                 break
        #             # Write into the local file the downloaded chunk.
        #             f.write(chunk)
        #             readBytes += chunkSize
        #             # Tell the window how many bytes we have received.
        #             self.setCurrentProgress.emit(readBytes)
        # If this line is reached then no exception has ocurred in
        # the previous lines.


    def run(self):
        readLocalFile("settings")
        settings = readLocalFile.data

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

        if self.whichCalendar == "All":
            for c in settings["CALENDARS"]:
                calendarsToSync.append(str(c))
        else:
            calendarsToSync.append(self.whichCalendar)

        self.setTotalProgress.emit(len(calendarsToSync))

        numberOfCalendarsWorked = 1
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
                                cat = upstreamTask[keyToUpdate].to_ical().decode()
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
            self.setCurrentProgress.emit(numberOfCalendarsWorked)
            numberOfCalendarsWorked = numberOfCalendarsWorked + 1
                
            # remove tasks marked completed upstream from todos dict
            # then add them to the completedTodos dict
            # TODO check if local completedTodos    are deleted from the server
        self.setCurrentTask.emit("Removing Completed Tasks")

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

        upstreamTagUidList.clear()

        changeLocalData(None, "completedTodos")
        changeLocalData(modifiedcompletedTasks, "completedTodos")
        changeLocalData(None, "todos")
        changeLocalData(modifiedTasks, "todos")
        changeLocalData(None, "tags")
        changeLocalData(modifiedTags, "tags")
        print("Sync Completed for calendar \"" + str(calendar) + "\".")

        # tagCheck()
        self.succeeded.emit()