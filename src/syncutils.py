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

            # Is the tag for current task in "tags" or "oldTags?", if not make a new entry in both
            # New Tag
            if value["CATEGORIES"] not in modifiedTags.keys() and value["CATEGORIES"] not in modifiedOldTags.keys():
                modifiedTags[value["CATEGORIES"]] = {}
                modifiedOldTags[value["CATEGORIES"]] = {}
            
            # Is the tag for current task in "tags" but not "oldTags?", if not then copy the entry to "oldTags"
            # Delete Tag
            elif value["CATEGORIES"] in modifiedTags.keys() and value["CATEGORIES"] not in modifiedOldTags.keys():
                modifiedOldTags[value["CATEGORIES"]] = modifiedTags[value["CATEGORIES"]]
            
            # Is the tag for current task not in "tags" but is "oldTags?", if not then copy the entry to "tags"
            # Restore Tag
            elif value["CATEGORIES"] not in modifiedTags.keys() and value["CATEGORIES"] in modifiedOldTags.keys():
                modifiedTags[value["CATEGORIES"]] = modifiedOldTags[value["CATEGORIES"]]
                
            if localTagList.count(value["CATEGORIES"]) == 0:
                localTagList.append(value["CATEGORIES"])

    for tag in tags.keys():
        if tag not in localTagList:
            del modifiedTags[tag]

    changeLocalData(None, "tags")
    changeLocalData(modifiedTags, "tags")
    changeLocalData(None, "oldTags")
    changeLocalData(modifiedOldTags, "oldTags")


def lastFullSyncCheck():
    readLocalFile("settings")
    settings = readLocalFile.data
    lastsync = settings["LASTSYNC"]
    if(lastsync != ""):
    
        formattedLastSync = datetime.strptime(lastsync, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        timeDifference = now - formattedLastSync
        if (timeDifference > timedelta(hours=4)):
            return True
