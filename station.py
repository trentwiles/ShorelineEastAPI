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
    r = requests.get()

    return