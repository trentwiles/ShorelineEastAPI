import requests
from bs4 import BeautifulSoup
import datetime
import time
import json

STATIONS_ID_TO_NAME = {
    "1": "New London",
    "2": "Old Saybrook",
    "3": "Westbrook",
    "4": "Clinton",
    "5": "Madison",
    "6": "Guilford",
    "7": "Branford",
    "8": "New Haven State Street",
    "9": "New Haven Union Station"
}

STATIONS_NAME_TO_ID = {
    "New London": "1",
    "Old Saybrook": "2",
    "Westbrook": "3",
    "Clinton": "4",
    "Madison": "5",
    "Guilford": "6",
    "Branford": "7",
    "New Haven State Street": "8",
    "New Haven Union Station": "9"
}

WESTERN_TERMINUS = "New Haven Union Station"
WESTERN_TERMINUS_ID = "9"
EASTERN_TERMINUS = "New London"
EASTERN_TERMINUS_ID = "1"

USER_AGENT = json.loads(open("config.json").read())["USER_AGENT"]

def formatDate(date):
    # Shoreline East wants dates to look like this:
    # 04/01/2024
    # 
    # Which is a bit of a problem because Python prints
    # out dates like this:
    # 4/1/2024
    #
    # This code will fix that

    if int(date) >= 10:
        return date
    
    return f"0{date}"

def formatTime(tme):
    if int(tme) > 12:
        return str(int(tme) - 12)
    return tme

def parseTime(rawTime, day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)

    sepHourAndMin = rawTime.split(":")
    minAndAMPM = sepHourAndMin[1].split(" ")
    
    hour = int(sepHourAndMin[0])
    minute = int(minAndAMPM[0])
    amPM = minAndAMPM[1]

    # Should convert 7:00 AM to 160000 or something like that
    # shorelineTimeToEpoch(5, "PM", 10, 3, 2024) = 166000000
    if amPM == "PM":
        if hour != 12:
            hour += 12

        if hour == 24:
            hour = 12
    else:
        if hour == 12:
            hour = 0

    ts = datetime.datetime(year, month, day, hour, minute)

    return int(ts.timestamp())


def translateStationToId(name):
    stations = STATIONS_NAME_TO_ID

    if name in stations:
        return stations[name]
    else:
        return None

def translateIDtoStation(id):
    stations = STATIONS_ID_TO_NAME
    if id in stations:
        return stations[id]
    else:
        return None
    
def getCallingAt(direction, fromStation):
    # WARNING: THIS ISN'T 100% ACCURATE
    # TRAINS SKIP SOME STATIONS
    # SEE THIS PDF: https://shorelineeast.com/wp-content/uploads/2024/04/SLE_Sched_Apr7_8R2.pdf
    terminatesAt = ""
    if direction.lower() == "westbound":
        stations = {key: value for key, value in reversed(STATIONS_NAME_TO_ID.items())}
        terminatesAt = WESTERN_TERMINUS
        if fromStation == WESTERN_TERMINUS:
            stations = []

    elif direction.lower() == "eastbound":
        stations = STATIONS_NAME_TO_ID
        terminatesAt = EASTERN_TERMINUS
        if fromStation == EASTERN_TERMINUS:
            stations = []

    else:
        return None

    
    cA = []
    for station in stations:
        if fromStation == station:
            break
        cA.append(station)

    cA.reverse()

    return {"currentStation": fromStation, "direction": direction, "callingAt": cA, "terminatesAt": terminatesAt}
        

def getAllTrainsAtStation(requestedTime:int, stationName:str, showPastTrains:bool):
    generatedAt = round(time.time())
    # get the station ID
    stationID = translateStationToId(stationName)
    if stationID == None:
        return None
    
    # convert timestamp
    dt = datetime.datetime.fromtimestamp(requestedTime)
    year = str(dt.year)
    month = str(dt.month)
    day = str(dt.day)
    print("day:" + day)
    hour = str(dt.hour)
    amPM = 'AM' if int(hour) < 12 else 'PM'
    minute = str(dt.minute)

    # IMPORTANT: NEED METHODS TO DETERMINE IF THE STATION INPUTTED IS THE TERMINUS

    dataTravelDate = f"{formatDate(month)}/{formatDate(day)}/{year}"
    dataTime = f"{formatTime(hour)}:{formatDate(minute)}+{amPM}"

    westboundData = {
        "fromstation": stationID,
        "tostation": WESTERN_TERMINUS_ID,
        "travel_date": dataTravelDate,
        "way": "2", # no idea what this is
        "time": dataTime,
        "return": "false" # one way only
    }
    eastboundData = {
        "fromstation": stationID,
        "tostation": EASTERN_TERMINUS_ID,
        "travel_date": dataTravelDate,
        "way": "2", # no idea what this is
        "time": dataTime,
        "return": "false" # one way only
    }
    def getTimesHelper(postData):
        r = requests.post("https://shorelineeast.com/schedules/trip-planner", data=postData, headers={"User-agent": USER_AGENT})
        se = BeautifulSoup(r.text, "html.parser")
        times = []
        for train in se.find_all("div", {"class": "result_box long"}):
            if train != None and "Depart" in train.text:
                time = train.text.strip("Depart at:").strip()
                times.append(time)

        return times
    
    def addEpochTime(timesFromAbove):
        detailedTimes = []
        for t in timesFromAbove:
            epochTime = parseTime(t, str(dt.day), str(dt.month), str(dt.year))
            until = round((epochTime - generatedAt)/60)

            isInPast = True
            if until > 0:
                isInPast = False

            # if show past trains is turned off, and the train is in the past
            if (not showPastTrains) and not (epochTime > generatedAt):
                print("skipped train at " + t)
            else:
                detailedTimes.append({"epochTime": epochTime, "humanReadable": t, "minutesUntil": until, "inPast": isInPast})
        
        return detailedTimes
    

    if stationName == EASTERN_TERMINUS:
        eastbound = {}
    else:
        eastbound = {
            "times": addEpochTime(getTimesHelper(eastboundData)),
            "stops": getCallingAt("eastbound", stationName)
        }
    
    if stationName == WESTERN_TERMINUS:
        westbound = {}
    else:
        westbound = {
            "times": addEpochTime(getTimesHelper(westboundData)),
            "stops": getCallingAt("westbound", stationName)
        }

    return {
        "generatedAt": generatedAt,
        "showingPastTrains": showPastTrains,
        "eastbound": eastbound,
        "westbound": westbound
    }
    


#print(getAllTrainsAtStation(round(time.time()),"Branford"))