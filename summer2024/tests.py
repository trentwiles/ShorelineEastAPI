import api, time, json

#print(api.getCallingAt("eastbound", "New Haven Union Station"))
print(json.dumps(api.getAllTrainsAtStation(round(time.time()), "Madison", False)))
#print(api.parseTime("7:15 AM", 21, 4, 2024))