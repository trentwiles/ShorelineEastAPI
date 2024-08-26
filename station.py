import requests
from bs4 import BeautifulSoup

def getPageDetails(station):
    # first, convert the station name to the correct format
    # so "Branford" becomes branford, and "New Haven Union Station" becomes union-station-new-haven
    stationToStationPage = {
        'New Haven Union Station': 'union-station-new-haven',
        'New Haven State Street Station': 'state-street-station-new-haven',
        'Branford': 'branford-station',
        'Guilford': 'guilford-station',
        'Madison': 'madison-station',
        'Clinton': 'clinton-station',
        'Westbrook': 'westbrook-station',
        'Old Saybrook': 'old-saybrook-station',
        'New London': 'new-london-station'
    }
    
    try:
        formatStation = stationToStationPage[station]
    except KeyError:
        return {"error": True, "message": "Invalid station name"}
    
    r = requests.get(f"https://shorelineeast.com/stations/{formatStation}/")
    soup = BeautifulSoup(r.text, "html.parser")
    counter = 1
    
    # Guide to WPB wraper
    # 1 & 2 - Name & Title (https://trentwil.es/a/eYhC8LxyIG.png)
    # 3 - Photo (https://trentwil.es/a/uDYgWjIqWg.png)
    # 4 & 5 - Address + Ticket Sales + Accessability (https://trentwil.es/a/Ou7cNK4xw9.png)
    # 6 & 7 - Trip Planning Button (https://trentwil.es/a/UKtxZEnbdo.png)
    # 8 & 9 - Elevator status, station information, bus substitution, parking, directions (https://trentwil.es/a/VJtQMsJbUw.png)
    # 10 - Directions
    # 11 & 12 - Trip planning
    
    for x in soup.find_all("div", {"class": "wpb_wrapper"}):
        print(f"{str(counter)}. ================================================")
        print(x)
        counter += 1
        

    return