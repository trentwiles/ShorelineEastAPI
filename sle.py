from bs4 import BeautifulSoup
import requests
from datetime import datetime

def time_difference_in_minutes(time1, time2):
    time_format = '%I:%M %p'
    datetime1 = datetime.strptime(time1, time_format)
    datetime2 = datetime.strptime(time2, time_format)

    try:
        datetime1 = datetime.strptime(time1, time_format)
        datetime2 = datetime.strptime(time2, time_format)
    except ValueError:
        return "Invalid time format"

    time_delta = datetime2 - datetime1
    minutes_difference = time_delta.total_seconds() / 60

    return round(minutes_difference)
def stationNameToStationNumber(name):
    dictionary = {
        "New London": 1,
        "Old Saybrook": 2,
        "Westbrook": 3,
        "Clinton": 4,
        "Madison": 5,
        "Guilford": 6,
        "Branford": 7,
        "New Haven State Street Station": 8,
        "New Haven Union Station": 9
    }
    return dictionary[name]

def getTrainHTML(startStation, endStation, travelDate, travelTimed):

    url = "https://shorelineeast.com/schedules/trip-planner"
    headers = {}

    terminus = "New Haven Union"
    if (stationNameToStationNumber(startStation) - stationNameToStationNumber(endStation)) > 0:
        terminus = "New London"

    data = {
        "fromstation": stationNameToStationNumber(startStation),
        "tostation": stationNameToStationNumber(endStation),
        "travel_date": travelDate,
        "way": "2",
        "time": travelTimed,
        "return": "false",
    }

    response = requests.post(url, data=data)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    trains = table.find_all("td")

    departTimes = []
    trainIDs = []

    travelTime = []
    arrivalTimes = []

    counter = 0
    for train in trains:
        if (counter % 3) == 0: # only get every third item, those have the valuable times
            departTimes.append(train.get_text(strip=True)[:-4])
            trainIDs.append(train.find("span").text.strip())
        elif "AM" in train.text or "PM" in train.text:
            arrivalTimes.append(train.text.strip())
        else:
            travelTime.append(train.text.strip())
        counter += 1
    
    final = []
    for x in range(len(travelTime)):
        final.append({"terminus": terminus, "trainNumber": trainIDs[x], "trainTime": departTimes[x], "timeTimeArrive": arrivalTimes[x], "trainTravelTime": travelTime[x], "timeFromUserRequest": time_difference_in_minutes(travelTimed, departTimes[x])})
    
    return final
    

print(getTrainHTML("Guilford", "Madison", "10/30/2023", "1:00 AM"))