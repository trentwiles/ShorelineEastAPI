import requests
from bs4 import BeautifulSoup

def getServiceAlerts():
    r = requests.get("https://shorelineeast.com/service-alerts/")
    soup = BeautifulSoup(r.text, "html.parser")

    alertsText = []
    alertsTitles = []

    feed = soup.find("div", {"class": "alert-feed"})

    allAlertsText = feed.find_all("p", {"class": "alert-text"})
    for x in allAlertsText:
        alertsText.append(x.text.strip())
    
    allAlertsTitles = feed.find_all("h3", {"class": "alert-title"})
    for x in allAlertsTitles:
        alertsTitles.append(x.text.strip())

    final = []
    for x in range(len(alertsTitles)):
        final.append({"title": alertsTitles[x], "content": alertsText[x]})
    
    return final