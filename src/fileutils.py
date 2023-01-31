
import json
import os
from datetime import date, datetime
import random
import davconnect

dataFile = "src/localData.json"
settingsAr = {"URL": "", "USERNAME": "", "PASSWORD": "", "CALENDARS": ""}
stockData = {"settings": settingsAr, "tags": {}, "todos": {}}

# This takes a dictionary and updates the key in local json
# changeLocalData(dict, key) commits the new dict to json for key
# changeLocalData(None, key) commits a blank dict to json for key


def changeLocalData(dict, key):
    if os.path.exists(dataFile):
        if dict == None:
            emptyDict = {}
            with open(dataFile, "r") as read_content:
                localdata = json.load(read_content)
                localdata[key] = emptyDict
                with open(dataFile, "w") as outfile:
                    json.dump(localdata, outfile, indent=4)

        if dict != None:
            with open(dataFile, "r") as read_content:
                localdata = json.load(read_content)
                if key in localdata.keys():
                    localdata[key].update(dict)
                    with open(dataFile, "w") as outfile:
                        json.dump(localdata, outfile, indent=4)

                else:
                    data = {key: dict}
                    with open(dataFile, "w") as outfile:
                        json.dump(data, outfile, indent=4)

    else:
        with open(dataFile, "w") as outfile:
            json.dump(stockData, outfile, indent=4)

# This reads the dict or list from local json


def readLocalFile(key):
    readLocalFile.data = {}
    if os.path.exists(dataFile):
        with open(dataFile, "r") as read_content:
            localdata = json.load(read_content)

            if key in localdata.keys():
                readLocalFile.data = localdata[key]
            else:
                print("No key to load")
    else:
        with open(dataFile, "w") as outfile:
            json.dump(stockData, outfile, indent=4)


def createTodo(tag, summary, due, uid, cal):
    readLocalFile("tags")
    tags = readLocalFile.data
    newTag = tags.copy()

    readLocalFile("todos")
    todos = readLocalFile.data

    key = "todos"
    num = random.randint(200, 15000)
    num2 = random.randint(200, 15000)

    newTodoData = {
        "SUMMARY": summary,
        "INCALENDAR": cal
    }

    if due != None:
        newTodoData["DUE"] = str(due)
    if tag != None:
        newTodoData["CATEGORIES"] = tag

        if tag not in tags.keys():
            newTag[tag] = {}
            changeLocalData(newTag, "tags")
    if uid != None:
        newTodoData["UID"] = uid
        deleteTodoByUID(uid)
    if uid == None:
        newTodoData["UID"] = str(num)
    newTodo = {
        num2: newTodoData
    }

    changeLocalData(newTodo, key)

# seach for a todo in the local json by uid, then delete the number assigned to it
# then rebuild the array and renumber the remaining todos


def deleteTodoByUID(uid):
    readLocalFile("tags")
    tags = readLocalFile.data
    newTag = tags.copy()

    newDict = {}
    delDict = {}
    readLocalFile("todos")
    todos = readLocalFile.data
    localTodos = todos.copy()

    i = 0
    for x, y in todos.items():
        if uid in y.values():
            delDict["INCALENDAR"] = y["INCALENDAR"]
            if "CATEGORIES" in y.keys():
                delDict["CATEGORIES"] = y["CATEGORIES"]
            delDict["UID"] = uid
            i = x

    j = 0
    del localTodos[i]
    for t, v in localTodos.items():
        newDict[j] = v
        j = j + 1

    tagExist = False
    for t in newDict.values():
        if "CATEGORIES" in t:
            if "CATEGORIES" in delDict.keys():
                if delDict["CATEGORIES"] == t["CATEGORIES"]:
                    tagExist = True

    if tagExist == False:
        if "CATEGORIES" in delDict.keys():
            del newTag[delDict["CATEGORIES"]]
            changeLocalData(None, "tags")
            changeLocalData(newTag, "tags")

    changeLocalData(None, "todos")
    changeLocalData(newDict, "todos")


def sortTodos(byWhat, direction):
    readLocalFile("todos")
    todos = readLocalFile.data

    if byWhat == "Due Date":
        deltaList = []
        for t in todos.values():
            if "DUE" in t.keys():
                rawDate = t["DUE"]
            else:
                rawDate = None

            if rawDate != None:
                today = date.today()
                formattedDate = datetime.strptime(rawDate, 'date(%Y, %m, %d)')
                delta = formattedDate.date() - today
                deltaList.append(delta.days)

        if direction == "Ascending":
            newTaskDict = {}
            deltaList.sort()
            i = 0
            for x in deltaList:
                for key, value in todos.copy().items():
                    if "DUE" in value.keys():
                        rawDate = value["DUE"]
                    else:
                        rawDate = None

                    if rawDate != None:
                        if "DUE" in value.keys():
                            today = date.today()
                            formattedDate = datetime.strptime(rawDate, 'date(%Y, %m, %d)')
                            delta = formattedDate.date() - today

                            if x == delta.days:
                                newTaskDict[i] = value
                                del todos[key]
                                i = i + 1

        if direction == "Descending":
            newTaskDict = {}
            deltaList.sort(reverse=True)
            i = 0
            for x in deltaList:
                for key, value in todos.copy().items():
                    if "DUE" in value.keys():
                        rawDate = value["DUE"]
                    else:
                        rawDate = None

                    if rawDate != None:
                        if "DUE" in value.keys():
                            today = date.today()
                            formattedDate = datetime.strptime(rawDate, 'date(%Y, %m, %d)')
                            delta = formattedDate.date() - today

                            if x == delta.days:
                                newTaskDict[i] = value
                                del todos[key]
                                i = i + 1
                
        for t in todos.values():
            if "DUE" not in t.keys():
                newTaskDict[i] = t
                i = i + 1
        changeLocalData(None, "todos")
        changeLocalData(newTaskDict, "todos")

    if byWhat == "Tag":
        changeLocalData(None, "todos")

        tagsList = []
        newTaskDict = {}
        for t in todos.values():
            if "CATEGORIES" in t.keys():
                tag = t["CATEGORIES"]
                tagsList.append(tag)

        if direction == "Ascending":
            tagsList.sort()
            i = 0
            for x in tagsList:
                for key, value in todos.copy().items():
                    if "CATEGORIES" in value.keys():

                        if value["CATEGORIES"] == x:
                            newTaskDict[i] = value
                            i = i + 1
                            del todos[key]

        if direction == "Descending":
            tagsList.sort(reverse=True)
            i = 0
            for x in tagsList:
                for key, value in todos.copy().items():
                    if "CATEGORIES" in value.keys():

                        if value["CATEGORIES"] == x:
                            newTaskDict[i] = value
                            i = i + 1
                            del todos[key]

        for t in todos.values():
            if "CATEGORIES" not in t.keys():
                newTaskDict[i] = t
                i = i + 1

        changeLocalData(newTaskDict, "todos")
