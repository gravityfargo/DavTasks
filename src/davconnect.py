import sys
from datetime import date
from datetime import datetime
from fileutils import *

## We'll try to use the local caldav library, not the system-installed
sys.path.insert(0, "..")
sys.path.insert(0, ".")

import caldav


def serverConnect():  
    readLocalFile("settings")
    settings = readLocalFile.data
    if settings["URL"] and settings["USERNAME"] and settings["PASSWORD"]:
        caldav_url = settings["URL"]
        username = settings["USERNAME"]
        password = settings["PASSWORD"]
        serverConnect.calendar = settings["CALENDARS"]
        client = caldav.DAVClient(url=caldav_url, username=username, password=password)
        serverConnect.my_principal = client.principal()
        getCalendars()
    else:
        return False
        
def getCalendars():
    calendarDict = {}
    finalCalendarsDict = {}
    calendars = serverConnect.my_principal.calendars()
    if calendars:
        for c in calendars:
            calendarDict[c.name] = str(c.url)
    else:
        print("your principal has no calendars")
    finalCalendarsDict["CALENDARS"] = calendarDict

    changeLocalData(finalCalendarsDict, "settings")


def pushUpstream(newTask, io):
    serverConnect()
    readLocalFile("tags")
    tags = readLocalFile.data
    
    tasksCalendar = newTask["INCALENDAR"]
    my_tasklist = serverConnect.my_principal.calendar(tasksCalendar)
    tasks = my_tasklist.todos()
    if "DUE" in newTask.keys():
        nDS = datetime.strptime(newTask["DUE"], 'date(%Y, %m, %d)')
        formattedDate = nDS.date()
        print(nDS)
    if io == "Create":
        if "CATEGORIES" in newTask.keys() and "DUE" in newTask.keys():
            my_tasklist.add_todo(
                summary=newTask["SUMMARY"],
                due=formattedDate,
                categories=[newTask["CATEGORIES"]]
            )
            tags[newTask["CATEGORIES"]] = {}
            changeLocalData(tags, "tags")
        elif "CATEGORIES" in newTask.keys() and "DUE" not in newTask.keys():
            my_tasklist.add_todo(
                summary=newTask["SUMMARY"],
                categories=[newTask["CATEGORIES"]]
            )
            tags[newTask["CATEGORIES"]] = {}
            changeLocalData(tags, "tags")
        elif "CATEGORIES" not in newTask.keys() and "DUE" in newTask.keys():
            my_tasklist.add_todo(
                summary=newTask["SUMMARY"],
                due=formattedDate
            )
        else:
            my_tasklist.add_todo(
                summary=newTask["SUMMARY"]
            )
    
    # todos_found = my_tasklist.search(
    #     todo=True,
    #     uid=existingTask["UID"],
    # )
    # if not todos_found:
    #     print(
    #         "Apparently your calendar server does not support searching for future instances of reoccurring tasks"
    #     )
    # else:
    #     print("Here is even more icalendar data:")
    #     print(todos_found[0].data)
    #     todos_found[0].complete()
        
  
    
     # pulls raw caldav data from server and formats into a dict
def pullUpstreamData():
    readLocalFile("settings")
    settings = readLocalFile.data
    serverConnect()

    if hasattr(serverConnect, "my_principal"):
        calendars = settings["CALENDARS"]
        finalTaskDict = {}
        finalTagsDict = {}

        i = 0
        j = 0
        for cal in calendars:
            my_tasklist = serverConnect.my_principal.calendar(name=cal)
            todos = my_tasklist.todos()   
            
            rawTagsList = []
            removedNoneTagsList = []
            intermediate_Tag_Dict = {}
            
            # DUE;TZID=America/New_York:20230207T140000
            # I need to add another split function specifically for the semicolons for recursion
            # Formats the raw caldav data into a usable dict
            
            for a in todos:
                a_Dict = {}
                a_split = a.data.split('\n')
                
                for e in a_split:
                    item = e.split(":", 1)          
                    if len(item) == 2:
                        a_Dict[str(item[0])] = str(item[1])
                        a_Dict["INCALENDAR"] =  cal
                        if "DUE" in a_Dict.keys():
                            # 20230129T200000
                            if len(a_Dict["DUE"]) == 15:
                                nDS = datetime.strptime(a_Dict["DUE"], '%Y%m%dT%H%M%S')
                                finalDate = nDS.date().strftime("date(%Y, %m, %d)")
                                a_Dict["DUE"] = finalDate
                        if "DUE;VALUE=DATE" in a_Dict.keys():
                            # 20000101
                            if len(a_Dict["DUE;VALUE=DATE"]) == 8:
                                nDS = datetime.strptime(a_Dict["DUE;VALUE=DATE"], '%Y%m%d')
                                finalDate = nDS.date().strftime("date(%Y, %m, %d)")
                                a_Dict["DUE"] = finalDate
                                del a_Dict["DUE;VALUE=DATE"]
                              
                finalTaskDict.update({i: a_Dict})
                rawTagsList.append(a_Dict.get("CATEGORIES"))  
                i = i + 1 

            # remove 'None' values
            for n in rawTagsList:
                if n != None:
                    removedNoneTagsList.append(n)
            # add the tags to a list
            for n in removedNoneTagsList:
                tags = n.split(',')
                for t in tags:
                    finalTagsDict[t] = intermediate_Tag_Dict
                j = j + 1

    return finalTaskDict, finalTagsDict 

