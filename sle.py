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

def flip_dict(input_dict):
    flipped_dict = {}
    for key, value in input_dict.items():
        flipped_dict[value] = key
    return flipped_dict

def getTrainDB():
    return {
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
def stationNameToStationNumber(name):
    dictionary = getTrainDB()
    try:
        return dictionary[name]
    except:
        return -1

def getTrainHTML(startStation, endStation, travelDate, travelTimed):

    if stationNameToStationNumber(startStation) == -1 or stationNameToStationNumber(endStation) == -1:
        return {"error": True, "message": "Invalid station name(s)"}

    url = "https://shorelineeast.com/schedules/trip-planner"
    headers = {}

    terminus = "New Haven Union"
    if (stationNameToStationNumber(startStation) - stationNameToStationNumber(endStation)) > 0:
        terminus = "New London"

    data = {
        "fromstation": str(stationNameToStationNumber(startStation)),
        "tostation": str(stationNameToStationNumber(endStation)),
        "travel_date": travelDate,
        "way": "2",
        "time": travelTimed,
        "return": "false",
    }

    print(data)

    response = requests.post(url, data=data)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    
    # Before anything, we need to make sure there was a valid request and the user
    # didn't screw up (ie. invalid date/time) that would invoke an invalid response
    # from SLE
    
    # Before we check all train times, we need to make sure there ARE train times
    # Somtimes, SLE will show an error message when the date you have selected is
    # to far in advance (example: https://trentwil.es/a/TwFwChF7yu.png)
    #
    # This line here will check if the page lacks the "Your Trip Itinerary" text,
    # meaning that the request is a failure, hence SLE cannot predict so far out
    tripHeading = soup.find("div", {"class": "trip_heading"})
    if "Your Trip Itinerary" not in tripHeading.text:
        return {"trains": None, "success": False, "message": "There is an anticipated schedule change occurring before the date you selected. We advise checking back closer to your travel date or call us at 1-877-CTrides (1-877-287-4337) for more information."}
    
    
    # Find all train times
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
        try:
            timeToTrain = time_difference_in_minutes(travelTimed, departTimes[x])
        except ValueError:
            return {"trains": None, "success": False, "message": "Invalid time, did you use the correct format? (examples: 10:00+AM, 10:00+PM, 01:00+AM, 04:00+PM)"}
        final.append({"terminus": terminus, "trainNumber": trainIDs[x], "trainTime": departTimes[x], "timeTimeArrive": arrivalTimes[x], "trainTravelTime": travelTime[x], "timeFromUserRequest": timeToTrain})
    
    return {"trains": final, "success": True}

def getAllTrains(startStation, travelDate, travelTimed):
    number = stationNameToStationNumber(startStation) # let's say that the station was station #6
    reverseTrains = flip_dict(getTrainDB())
    
    westStation = number + 1
    eastStation = number - 1

    # If the train station is New London, then don't find trains going past NL ("eastbound")
    if number == 1:
        return {"error": False, "east": getTrainHTML(startStation, reverseTrains[eastStation], travelDate, travelTimed), "west": {"trains": []}}
    
    # If the train station is New Haven, then don't find trains going past NH ("westbound")
    if number == 9:
        return {"error": False, "east": {"trains": []}, "west": getTrainHTML(startStation, reverseTrains[westStation], travelDate, travelTimed)}
    
    return {"error": False, "east": getTrainHTML(startStation, reverseTrains[eastStation], travelDate, travelTimed), "west": getTrainHTML(startStation, reverseTrains[westStation], travelDate, travelTimed)}