import requests
from bs4 import BeautifulSoup

def getPageDetails(station):
    # first, convert the station name to the correct format
    # so "Branford" becomes branford, and "New Haven Union Station" becomes union-station-new-haven

    r = requests.get()

    return