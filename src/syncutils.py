from fileutils import *
from davconnect import *
from datetime import datetime, timedelta


def tagCheck():
    readLocalFile("tags")
    tags = readLocalFile.data
    modifiedTags = tags.copy()

    readLocalFile("oldTags")
    oldTags = readLocalFile.data
    modifiedOldTags = oldTags.copy()

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


def lastFullSyncCheck():
    readLocalFile("settings")
    settings = readLocalFile.data

    lastsync = settings["LASTSYNC"]
    formattedLastSync = datetime.strptime(lastsync, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()

    timeDifference = now - formattedLastSync

    if (lastsync == "" or timeDifference > timedelta(hours=4)):
        return True
