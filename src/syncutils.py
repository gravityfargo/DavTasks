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
            task.icalendar_component["DTSTART"] = formattedDate
            task.icalendar_component["DUE"] = formattedDate

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
