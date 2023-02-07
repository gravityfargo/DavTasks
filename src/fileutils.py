import json
import os
from datetime import date, datetime

dataFile = "./src/localData.json"
settingsAr = {"URL": "", "USERNAME": "", "PASSWORD": "", "CALENDARS": ""}
stockData = {"settings": settingsAr, "tags": {},
             "todos": {}, "completedTodos": {}}

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


# seach for a todo in the local json by uid, then delete the number assigned to it
# then rebuild the array and renumber the remaining todos


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
                formattedDate = datetime.strptime(rawDate, '%Y-%m-%d %H:%M:%S')
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
                            formattedDate = datetime.strptime(
                                rawDate, '%Y-%m-%d %H:%M:%S')
                            delta = formattedDate.date() - today

                            if x == delta.days:
                                newTaskDict[key] = value
                                del todos[key]

        if direction == "Descending":
            newTaskDict = {}
            deltaList.sort(reverse=True)
            for x in deltaList:
                for key, value in todos.copy().items():
                    if "DUE" in value.keys():
                        rawDate = value["DUE"]
                    else:
                        rawDate = None

                    if rawDate != None:
                        if "DUE" in value.keys():
                            today = date.today()
                            formattedDate = datetime.strptime(
                                rawDate, '%Y-%m-%d %H:%M:%S')
                            delta = formattedDate.date() - today

                            if x == delta.days:
                                newTaskDict[key] = value
                                del todos[key]

        for key, value in todos.copy().items():
            if "DUE" not in value.keys():
                newTaskDict[key] = value

        return newTaskDict

    if byWhat == "Tag":

        tagsList = []
        newTaskDict = {}
        for t in todos.values():
            if "CATEGORIES" in t.keys():
                tag = t["CATEGORIES"]
                tagsList.append(tag)

        if direction == "Ascending":
            tagsList.sort()
            for x in tagsList:
                for key, value in todos.copy().items():
                    if "CATEGORIES" in value.keys():
                        if value["CATEGORIES"] == x:
                            newTaskDict[key] = value
                            del todos[key]

        if direction == "Descending":
            tagsList.sort(reverse=True)
            for x in tagsList:
                for key, value in todos.copy().items():
                    if "CATEGORIES" in value.keys():

                        if value["CATEGORIES"] == x:
                            newTaskDict[key] = value
                            del todos[key]

        for key, value in todos.copy().items():
            if "CATEGORIES" not in value.keys():
                newTaskDict[key] = value

        return newTaskDict


def filterByTags(tagSortFilter):
    readLocalFile("todos")
    todos = readLocalFile.data
    newTaskDict = {}

    for key, value in todos.copy().items():
        if "CATEGORIES" in value.keys():
            if value["CATEGORIES"] == tagSortFilter:
                newTaskDict[key] = value

    return newTaskDict
