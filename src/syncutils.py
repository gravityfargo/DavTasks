from fileutils import *
from davconnect import *

# If a tag exists upstream, it wont be deleted from json. New tags are added.


def compareData():

    pulledTasks, pulledTags = pullUpstreamData()
    print("Pull Complete")

    readLocalFile("tags")
    localTags = readLocalFile.data

    readLocalFile("todos")
    localTasks = readLocalFile.data

    syncedTags = {}
    syncedTodos = {}

    for pt in pulledTags:
        if pt not in localTags.keys():
            syncedTags[pt] = {}

    changeLocalData(syncedTags, "tags")

    i = 0
    for pt in pulledTasks.values():
        if pt not in localTasks.values():
            syncedTodos[i] = pt
            i = i + 1
    
    for lt in localTasks.values():
        syncedTodos[i] = lt
        i = i + 1
        

    changeLocalData(None, "todos")
    changeLocalData(syncedTodos, "todos")
