import api, time, json

#print(api.getCallingAt("eastbound", "New Haven Union Station"))
print(json.dumps(api.getAllTrainsAtStation(round(time.time()), "Madison")))