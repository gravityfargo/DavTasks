from fileutils import *
from davconnect import *
from icalendar.prop import vCategory, vDatetime
import uuid

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