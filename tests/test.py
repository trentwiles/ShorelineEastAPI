import requests
import re
import unittest

# Must be correct for tests to execute
API_SERVER = "http://localhost:10394"
class TestSum(unittest.TestCase):
    def testAlive(self):
        r = requests.get(f"{API_SERVER}/")
        assert (r.status_code == 200), "HTTP Status is 200"
        
    def testIDToStationOne(self):
        r = requests.get(f"{API_SERVER}/api/v1/stations/convertIDToStation/5")
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["stationName"] == "Madison")

    def testIDToStationTwo(self):
        r = requests.get(f"{API_SERVER}/api/v1/stations/convertIDToStation/9")
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["stationName"] == "New Haven Union Station")

    def testStationToIDOne(self):
        r = requests.get(f"{API_SERVER}/api/v1/stations/convertStationToID/Guilford")
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["stationID"] == "6")
        
    def testStationToIDTwo(self):
        stationName = "New London"
        # api docs specify that we must convert spaces to "-"
        stationName = re.sub(" ", "-", stationName)
        r = requests.get(f"{API_SERVER}/api/v1/stations/convertStationToID/{stationName}")
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["stationID"] == "1")

    def testFareOne(self):
        r = requests.post(
            f"{API_SERVER}/api/v1/fares/getRideFare",
            data={"start": "New London", "end": "New Haven Union Station", "isSenior": "false", "isOffPeak": "false", "ticketType": "one_way"}
        )
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["fare"] == "10.75")
    
    def testFareTwo(self):
        r = requests.post(
            f"{API_SERVER}/api/v1/fares/getRideFare",
            data={"start": "New Haven State Street", "end": "Westbrook", "isSenior": "false", "isOffPeak": "false", "ticketType": "one_way"}
        )
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["fare"] == "6.75")
    
    def testFareSeniorDiscount(self):
        r = requests.post(
            f"{API_SERVER}/api/v1/fares/getRideFare",
            data={"start": "Madison", "end": "Old Saybrook", "isSenior": "true", "isOffPeak": "false", "ticketType": "one_way"}
        )
        assert (r.status_code == 200), "HTTP Status is 200"
        assert (r.json()["fare"] == "2.25")
        # senior discount notice
        assert (r.json()["message"] != None)

if __name__ == '__main__':
    unittest.main()