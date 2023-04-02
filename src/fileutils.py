import sys
import subprocess
import pkg_resources
import json
import os
from datetime import date, datetime

# Make sure deps are installed
requiredPackages = {'caldav==1.2.1'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = requiredPackages - installed

if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

configFile = os.path.expanduser('~/.local/share/DavTasks/data.json')
configPath = os.path.expanduser('~/.local/share/DavTasks')

settingsAr = {"URL": "", "USERNAME": "",
              "PASSWORD": "", "CALENDARS": "", "ENABLEDCALENDARS": "", "DEFAULTCAL": "", "LASTSYNC": ""}

stockData = {"settings": settingsAr, "tags": {},
             "todos": {}, "completedTodos": {}, "oldTags": {}}

# This takes a dictionary and updates the key in local json
# changeLocalData(dict, key) commits the new dict to json for key
# changeLocalData(None, key) commits a blank dict to json for key


def changeLocalData(dict: dict, key: str):
    if os.path.exists(configFile):
        if dict == None:
            emptyDict = {}
            with open(configFile, "r") as read_content:
                localdata = json.load(read_content)
                localdata[key] = emptyDict
                with open(configFile, "w") as outfile:
                    json.dump(localdata, outfile, indent=4)

        if dict != None:
            with open(configFile, "r") as read_content:
                localdata = json.load(read_content)
                if key in localdata.keys():
                    localdata[key].update(dict)
                    with open(configFile, "w") as outfile:
                        json.dump(localdata, outfile, indent=4)

                else:
                    data = {key: dict}
                    with open(configFile, "w") as outfile:
                        json.dump(data, outfile, indent=4)

    else:
        createConfig()


# This reads local json
def readLocalFile(key: str):
    readLocalFile.data = {}
    if os.path.exists(configFile):
        with open(configFile, "r") as read_content:
            localdata = json.load(read_content)

            if key in localdata.keys():
                readLocalFile.data = localdata[key]
            else:
                print("No key to load")
    else:
        createConfig()


def createConfig():
    if not os.path.exists(configFile):
        os.makedirs(configPath)
        with open(configFile, "w") as outfile:

            json.dump(stockData, outfile, indent=4)
    else:
        json.dump(stockData, outfile, indent=4)


# seach for a todo in the local json by uid, then delete the number assigned to it
# then rebuild the array and renumber the remaining todos
def sortTodos(byWhat: str, direction: str):
    readLocalFile("todos")
    todos = readLocalFile.data

    if byWhat == "Due Date":
        deltaList = []
        newTaskDict = {}
        # goes through each todo, and if it has a due date, adds the delta to a list.
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
