import requests
import api

NORMAL_NAMES_TO_FARE_NAMES = {
    "New London": "newLondon",
    "Old Saybrook": "oldSaybrook",
    "Westbrook": "westbrook",
    "Clinton": "clinton",
    "Madison": "madison",
    "Guilford": "guilford",
    "Branford": "branford",
    "New Haven State Street": "newHaven",
    "New Haven Union Station": "newHaven"
}

ID_TO_FARE_TYPES = {
    "1": "newLondon",
    "2": "oldSaybrook",
    "3": "westbrook",
    "4": "clinton",
    "5": "madison",
    "6": "guilford",
    "7": "branford",
    "8": "newHaven",
    "9": "newHaven"
}

FARE_TYPES = {
    "One Way": "one_way",
    "Ten Trip": "ten_trip",
    "Monthly": "monthly",
    "Monthly Plus Bus": "monthly_bus",
    "School Monthly": "school_monthly"
}



def calculateFare(ticketType, isSenior, isOffPeak, start, end):
    data = {
        "ticket": ticketType,
        "senior": str(isSenior).lower(),
        "offPeak": str(isOffPeak).lower(),
        "startLoc": start,
        "endLoc": end
    }
    r = requests.post("https://shorelineeast.com/wp-content/themes/pressville-child/shortcodes/fare_calculator/include/results.php", data=data, headers={"User-agent": api.USER_AGENT})
    if r.text.strip() == "":
        return None
    return r.json()[0]

print(calculateFare("one_way", True, False, "newHaven", "newLondon"))