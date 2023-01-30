
import json
import os
from datetime import date, datetime
import random

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
    key = "todos"
    num = str(random.random())

    readLocalFile("todos")
    todos = readLocalFile.data

    lastKey = int(list(todos.keys())[-1]) + 1

    newTodoData = {
        "SUMMARY": summary,
        "UID": num,
        "INCALENDAR": cal
    }

    if due != None:
        newTodoData["DUE"] = str(due)
    if tag != None:
        newTodoData["CATEGORIES"] = tag
    if uid != None:
        deleteTodoByUID(uid)

    newTodo = {
        lastKey: newTodoData
    }
    changeLocalData(newTodo, key)

# seach for a todo in the local json by uid, then delete the number assigned to it
# then rebuild the array and renumber the remaining todos


def deleteTodoByUID(uid):
    newDict = {}
    readLocalFile("todos")
    todos = readLocalFile.data
    localTodos = todos.copy()
    i = 0
    for x, y in todos.items():
        if uid in y.values():
            i = x
    j = 0
    del localTodos[i]
    for t, v in localTodos.items():
        newDict[j] = v
        j = j + 1
    changeLocalData(None, "todos")
    changeLocalData(newDict, "todos")
