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


# def findCalendar(calName):
#     try:
#         my_calendar = serverConnect.my_principal.calendar(name=calName)
#         assert my_calendar
#     except caldav.error.NotFoundError:
#         print("Couldnt find the calendar.")
     
     # pulls raw caldav data from server and formats into a dict
def pullUpstreamData():
    readLocalFile("settings")
    settings = readLocalFile.data
    serverConnect()

    if hasattr(serverConnect, "my_principal"):
        calendars = settings["CALENDARS"]
        finalTaskDict = {}
        finalTagsDict = {}

        for cal in calendars:
            
            my_tasklist = serverConnect.my_principal.calendar(name=cal)
            todos = my_tasklist.todos()   
            
            rawTagsList = []
            removedNoneTagsList = []
            intermediate_Tag_Dict = {}

            i = 0
            # DUE;TZID=America/New_York:20230207T140000
            # I need to add another split function specifically for the semicolons for recursion
            # Formats the raw caldav data into a usable dict
            for a in todos:
                a_split = a.data.split('\n')
                a_Dict = {}
                for e in a_split:
                    item = e.split(":", 1)                
                    if len(item) == 2:
                        a_Dict.update({item[0]: item[1]})
                        a_Dict["INCALENDAR"] =  cal
                        
                    else:
                        nope = 1
                finalTaskDict.update({i: a_Dict})
                i = i + 1
                rawTagsList.append(a_Dict.get("CATEGORIES"))   
                
            # remove 'None' values
            for n in rawTagsList:
                if n != None:
                    removedNoneTagsList.append(n)
            # add the tags to a list
            i = 0
            for n in removedNoneTagsList:
                tags = n.split(',')
                for t in tags:
                    finalTagsDict[t] = intermediate_Tag_Dict
                i = i + 1

    return finalTaskDict, finalTagsDict 

