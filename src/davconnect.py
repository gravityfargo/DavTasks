import caldav
import sys
from fileutils import readLocalFile, changeLocalData

# We'll try to use the local caldav library, not the system-installed
sys.path.insert(0, "..")
sys.path.insert(0, ".")


def serverConnect():
    readLocalFile("settings")
    settings = readLocalFile.data
    if settings["URL"] and settings["USERNAME"] and settings["PASSWORD"]:
        with caldav.DAVClient(
            url=settings["URL"], username=settings["USERNAME"], password=settings["PASSWORD"]
        ) as client:

            serverConnect.my_principal = client.principal()


def getCalendars():
    serverConnect()
    calendars = serverConnect.my_principal.calendars()
    calendarDict = {}
    finalCalendarsDict = {}
    finalCalendarsDict["CALENDARS"] = ""
    changeLocalData(finalCalendarsDict, "settings")
    if calendars:
        for c in calendars:
            calendarDict[c.name] = str(c.url)
            finalCalendarsDict["CALENDARS"] = calendarDict
            changeLocalData(finalCalendarsDict, "settings")
