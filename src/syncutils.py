from fileutils import *
from davconnect import *
import main

# If a tag exists upstream, it wont be deleted from json. New tags are added.

def compareData(bool):
    pulledTasks, pulledTags = pullUpstreamData()

    
    readLocalFile("tags")
    localTags = readLocalFile.data

    readLocalFile("todos")
    localTasks = readLocalFile.data

    syncedTags = localTags.copy()
    syncedTasks = localTasks.copy()
    
    if len(localTasks) == 0:
        keyForNewTask = 0
    else:
        lastKey = int(list(localTasks.keys())[-1])
        keyForNewTask = lastKey + 1

    if bool == True:
        print("Pushing Upstream")
        i = 0
        # remove task from server that doesnt exit locally
        for pt in pulledTasks.values():
            if pt not in localTasks.values():
                pushUpstream(pt, "Delete")
                main.MainWindow().uidMoverDist[i] = pt["UID"]
                i = i + 1        
        # create task on server that doesnt exist on the server
        for lt in localTasks:
            if localTasks[lt] not in pulledTasks.values():
                davconnect.pushUpstream(localTasks[lt], "Create")
                
    
        print("Push Complete")
        
    if bool == False:
        print("Pulling from Upstream")
        
        # add tag from server that doesnt exist locally
        for pt in pulledTags:
            if pt not in localTags.keys():
                syncedTags[pt] = {}
        
        # Delete tag locally that doesnt exist on the server
        for lt in localTags:
            if lt not in pulledTags.keys():
                del syncedTags[lt]

        # Add task from server that doesnt exit locally
        for pt in pulledTasks.values():
            if pt not in localTasks.values():
                syncedTasks[keyForNewTask] = pt
                keyForNewTask = keyForNewTask + 1
        
        # Delete task locally that doesnt exist on the server
        for lt in localTasks:
            if localTasks[lt] not in pulledTasks.values():
                del syncedTasks[lt]
        print("Pull Complete")
            

        changeLocalData(None, "todos")
        changeLocalData(syncedTasks, "todos")
        
        changeLocalData(None, "tags")
        changeLocalData(syncedTags, "tags")
