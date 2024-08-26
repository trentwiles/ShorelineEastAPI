import requests
from bs4 import BeautifulSoup
import re

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
    
    if r.status_code != 200:
        return {"success": False, "message": f"Non 202 status code from SLE ({str(r.status_code)})", data: None}
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    wrappers = soup.find_all("div", {"class": "wpb_wrapper"})
    
    
    # Guide to WPB wraper
    # 1 & 2 - Name & Title (https://trentwil.es/a/eYhC8LxyIG.png)
    # 3 - Photo (https://trentwil.es/a/uDYgWjIqWg.png)
    three = wrappers[2]
    img = three.find("img")
    x_image = img.get('src')
    # 4 & 5 - Address + Ticket Sales + Accessability (https://trentwil.es/a/Ou7cNK4xw9.png)
    four = wrappers[3]
    x_address = four.find("h3").text
    x_address = re.sub('\n', ' ', x_address)
    fourTags = four.find_all("p")
    x_fare = fourTags[0].text.strip()
    x_access = fourTags[1].text.strip()
    # 6 & 7 - Trip Planning Button (https://trentwil.es/a/UKtxZEnbdo.png)
    # 8 & 9 - Elevator status, station information, bus substitution, parking, directions (https://trentwil.es/a/VJtQMsJbUw.png)
    eight = wrappers[7]
    eightTags = eight.find_all("p")
    
    x_elevator = eightTags[0].text.strip()
    x_station = eightTags[1].text.strip()
    x_busSub = eightTags[2].text.strip()
    x_connections = eightTags[3].text.strip()
    x_parking = eightTags[4].text.strip()
    
    # 10 - Directions
    # 11 & 12 - Trip planning
    
    data = {
        "image_url": x_image,
        "address": x_address,
        "ticket_sales": x_fare,
        "accessibility": x_access,
        "elevator": x_elevator,
        "station_information": x_station,
        "bus_substitution": x_busSub,
        "connections": x_connections,
        "parking": x_parking
    }

    return {"success": True, "data": data}