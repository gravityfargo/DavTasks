from fileutils import *
from davconnect import *
from icalendar.prop import vCategory, vDatetime
import uuid


# TODO if a completed task is modified, remove it from the completeTodos dict
# and readd it to the main dict


def modifyTodo(taskToModify, cal):
    readLocalFile("todos")
    tasks = readLocalFile.data
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
            nDS = datetime.strptime(taskToModify["DUE"], "%Y-%m-%d %H:%M:%S")
            formattedDate = vDatetime(nDS).to_ical()
            task.icalendar_component["due"] = formattedDate

        if "CATEGORIES" in taskToModify.keys():
            newCatList = []
            newCatList.append(taskToModify["CATEGORIES"])
            newCat = vCategory(newCatList).to_ical()
            task.icalendar_component["CATEGORIES"] = newCat

        task.save()
        serverSync(cal)


def createTodo(taskDict, cal):

    serverConnect()
    calendar = serverConnect.my_principal.calendar(cal)
    assert len(taskDict) > 0

    uidNew = str(uuid.uuid1())
    taskDict["UID"] = uidNew
    if "LAST-MODIFIED" not in taskDict.keys():
        nDS = datetime.now()
        formattedDate = nDS.strftime("%Y-%m-%d %H:%M:%S")
        taskDict["LAST-MODIFIED"] = formattedDate

    if "DUE" in taskDict.keys():
        nDS = datetime.strptime(taskDict["DUE"], "%Y-%m-%d %H:%M:%S")
        formattedDate = nDS.date()

    # TODO assigning a uid is broken in pydav, when it's fixed I'll have to reimplement
    # create the todo locally and remotely w/o calling for a syncpull

    if "CATEGORIES" in taskDict.keys() and "DUE" in taskDict.keys():
        calendar.add_todo(
            summary=taskDict["SUMMARY"],
            due=formattedDate,
            categories=[taskDict["CATEGORIES"]],
            # uid=uidNew
        )

    elif "CATEGORIES" in taskDict.keys() and "DUE" not in taskDict.keys():
        calendar.add_todo(
            summary=taskDict["SUMMARY"],
            categories=[taskDict["CATEGORIES"]],
            # uid=uidNew
        )

    elif "CATEGORIES" not in taskDict.keys() and "DUE" in taskDict.keys():
        calendar.add_todo(
            summary=taskDict["SUMMARY"],
            due=formattedDate,
            # uid=uidNew
        )
    else:
        calendar.add_todo(
            summary=taskDict["SUMMARY"],
            # uid=uidNew
        )
    # remove when uid is fixed
    serverSync(cal)


def tagCheck():
    readLocalFile("tags")
    tags = readLocalFile.data
    modifiedTags = tags.copy()

    readLocalFile("todos")
    tasks = readLocalFile.data

    localTagList = []

    for key, value in tasks.items():
        if "CATEGORIES" in value.keys():

            if value["CATEGORIES"] not in modifiedTags.keys():
                modifiedTags[value["CATEGORIES"]] = {}

            if localTagList.count(value["CATEGORIES"]) == 0:
                localTagList.append(value["CATEGORIES"])

    for tag in tags.keys():
        if tag not in localTagList:
            del modifiedTags[tag]

    changeLocalData(None, "tags")
    changeLocalData(modifiedTags, "tags")
    print("Tag check completed.")


def serverSync(whichCalendar):
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

    calendarToSync = []

    if whichCalendar == "All":
        for c in settings["CALENDARS"]:
            calendarToSync.append(c)
    else:
        calendarToSync.append(whichCalendar)

    upstreamTagUidList = []

    for calendar in calendarToSync:

        serverConnect()
        calendar = serverConnect.my_principal.calendar(calendar)
        todos = calendar.todos()

        for t in todos:
            upstreamTask = t.icalendar_component
            upstreamUID = upstreamTask["UID"]

            if upstreamUID in keys:
                upstreamTagUidList.append(upstreamUID.to_ical().decode())
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
                        if keyToUpdate == "LAST-MODIFIED" or keyToUpdate == "CREATED" or keyToUpdate == "DTSTAMP":
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
                upstreamTagUidList.append(upstreamUID.to_ical().decode())
                newTask = {}
                for keyToCreate in upstreamTask.keys():

                    if keyToCreate == "LAST-MODIFIED" or keyToCreate == "CREATED" or keyToCreate == "DTSTAMP":
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

        # remove tasks marked completed upstream from todos dict
        # then add them to the completedTodos dict
        # TODO check if local completedTodos are deleted from the server

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
    tagCheck()


def completeTodoSync(uid):
    readLocalFile("todos")
    todos = readLocalFile.data
    modifiedTodos = todos.copy()
    task = todos[uid]
    readLocalFile("completedTodos")
    completedTodos = readLocalFile.data
    modifiedCompletedTodos = completedTodos.copy()
    serverConnect()
    calendar = serverConnect.my_principal.calendar(task["INCALENDAR"])
    print(task["INCALENDAR"])
    taskFetched = calendar.search(
        todo=True,
        uid=uid
    )
    if taskFetched:
        modifiedCompletedTodos[uid] = task
        del modifiedTodos[uid]
        taskFetched[0].complete()
        print("Task marked completed.")

    changeLocalData(None, "todos")
    changeLocalData(modifiedTodos, "todos")

    changeLocalData(None, "completedTodos")
    changeLocalData(modifiedCompletedTodos, "completedTodos")
    
    serverSync(task["INCALENDAR"])
