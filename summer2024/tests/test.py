import requests

# Must be correct for tests to execute
API_SERVER = "http://localhost:5000"

def testAlive():
    r = requests.get(f"{API_SERVER}/")
    assert sum(r.status_code == 200, "HTTP Status is 200")
    

if __name__ == "__main__":
    testAlive()
    print("Tests Passed!")