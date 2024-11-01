import requests
from bs4 import BeautifulSoup
import json

USER_AGENT = json.loads(open("config.json").read())["USER_AGENT"]

def getStationInfo(name):
    website_stations = {
        "New London": "new-london-station",
        "Old Saybrook": "old-saybrook-station",
        "Westbrook": "westbrook-station",
        "Clinton": "clinton-station",
        "Madison": "madison-station",
        "Guilford": "guilford-station",
        "Branford": "branford-station",
        "New Haven State Street": "state-street-station-new-haven",
        "New Haven Union Station": "union-station-new-haven"
    }
    if name not in website_stations:
        return None
    
    r = requests.get(f"https://shorelineeast.com/stations/{website_stations[name]}/", headers={"User-agent": USER_AGENT})
    soup = BeautifulSoup(r.text, "html.parser")

    divs = soup.find_all("div", {"class": "wpb_wrapper"})
    for d in divs:
        print(d)
        print("--------------------------------------------")

# getStationInfo("New Haven Union Station")