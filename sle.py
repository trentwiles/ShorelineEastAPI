from bs4 import BeautifulSoup
import requests

def stationNameToStationNumber(number):
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
    return
def getTrainHTML(startStation, endStation, travelDate, travelTime):
    r = requests.post("https://shorelineeast.com/schedules/trip-planner", data={"fromStation": stationNameToStationNumber(startStation), "toStation": stationNameToStationNumber(endStation), "travel_date": travelDate, "way": 2, "time": travelTime, "return": "false"})
    print(r.status_code)    
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("th")

    print(table)

    for x in table.find("thead"):
        print(x)
        print("^^^^^^^^^^^^^^^^^^^^")


getTrainHTML("Madison", "Guilford", "10/25/2023", "7:00+AM")