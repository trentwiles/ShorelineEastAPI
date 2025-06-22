import requests
import api

# note: New Haven - State Street and New Haven Union Station are both considered the same station
#       under the current fare calculation scheme
NORMAL_NAMES_TO_FARE_NAMES = {
    "New London": "newLondon",
    "Old Saybrook": "oldSaybrook",
    "Westbrook": "westbrook",
    "Clinton": "clinton",
    "Madison": "madison",
    "Guilford": "guilford",
    "Branford": "branford",
    "New Haven State Street": "newHaven",
    "New Haven Union Station": "newHaven",
    # NON SLE STATIONS
    # -----------------------
    # Note that stations included and up to Stamford may see "thru" service
    "West Haven": "westHaven",
    "Bridgeport": "bridgeport",
    "South Norwalk": "southNorwalk",
    "Stamford": "stamford",
    "Harlem-125th St": "harlem",
    "Grand Central": "grandCentral"
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

def convertNameToFareHelper(normalName):
    if normalName not in NORMAL_NAMES_TO_FARE_NAMES:
        return None
    return NORMAL_NAMES_TO_FARE_NAMES[normalName]

def calculateFare(ticketType, isSenior, isOffPeak, start, end):
    # assuming start & end are not in the proper format
    start = convertNameToFareHelper(start)
    end = convertNameToFareHelper(end)

    if start == None or end == None:
        return None

    data = {
        "ticket": ticketType,
        "senior": str(isSenior).lower(),
        "offPeak": str(isOffPeak).lower(),
        "startLoc": start,
        "endLoc": end
    }
    r = requests.post("https://shorelineeast.com/wp-content/themes/pressville-child/shortcodes/fare_calculator/include/results.php", data=data, headers={"User-agent": api.USER_AGENT})
    
    # A failed result is blank
    if r.text.strip() == "":
        return None
    
    fare = r.json()[0]
    comment = r.json()[1]

    return {"fare": fare, "comment": comment, "currency": "USD"}

#print(calculateFare("one_way", True, False, "newHaven", "newLondon"))