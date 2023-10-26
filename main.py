from flask import Flask, render_template, Response
import sle
import json
import re
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ""

@app.route('/time/<station>')
def time(station):
    current_datetime = datetime.datetime.now()
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute

    if current_hour < 12:
        am_pm = "AM"
    else:
        am_pm = "PM"

    if current_hour > 12:
        current_hour -= 12

    theTime = f"{current_hour}:{current_minute} {am_pm}"
    return render_template("time.html", station=station, theTime=theTime)

@app.route('/board/<station>')
def board(station):
    current_datetime = datetime.datetime.now()
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_year = current_datetime.year
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute

    if current_hour < 12:
        am_pm = "AM"
    else:
        am_pm = "PM"

    if current_hour > 12:
        current_hour -= 12

    tD = f"{current_month}/{current_day}/{current_year}"
    tT = f"{current_hour}:{current_minute} {am_pm}"
    api = sle.getAllTrains(station, tD, tT)
    print(api)

    eastTrainsText = ""
    eastTrainsIDs = ""
    hasLeavingEast = False
    westTrainsText = ""
    westTrainsIDs = ""
    hasLeavingWest = False

    try:
        east = api["east"]["trains"]
        for train in east:
            if train["timeFromUserRequest"] > 0:
                eastTrainsText += "," + str(train["timeFromUserRequest"])
                eastTrainsIDs += "," + str(train["trainNumber"])
            if train["timeFromUserRequest"] == 0:
                hasLeavingEast = True
        west = api["west"]["trains"]
        for train in west:
            if train["timeFromUserRequest"] > 0:
                westTrainsText += "," + str(train["timeFromUserRequest"])
                westTrainsIDs += "," + str(train["trainNumber"])
            if train["timeFromUserRequest"] == 0:
                hasLeavingWest = True

    except:
        print("oops")
        
    
    eastTrainsText = eastTrainsText[1:]
    eastTrainsIDs = eastTrainsIDs[1:]
    westTrainsText = westTrainsText[1:]
    westTrainsIDs = westTrainsIDs[1:]


    return render_template("board.html", east=api["east"], west=api["west"], len=len, eastTrainsText = eastTrainsText, eastTrainsIDs=eastTrainsIDs, westTrainsText = westTrainsText, westTrainsIDs = westTrainsIDs, station=station)

@app.route('/api/v1/getStations')
def getStations():
    return Response(json.dumps({"error": False, "stationsToNumber": sle.getTrainDB(), "numbersToStation": sle.flip_dict(sle.getTrainDB())}), content_type="application/json")

@app.route('/api/v1/getPredictions/<station1>/<station2>/<travelDate>/<travelTime>')
def getPredictions(station1, station2, travelDate, travelTime):
    travelTime = re.sub(r'\+', ' ', travelTime)
    travelDate = re.sub(r'\+', '/', travelDate)
    api = sle.getTrainHTML(station1, station2, travelDate, travelTime)
    return Response(json.dumps({"error": False, "data": api}), content_type="application/json"), 200

@app.route('/api/v1/getAllTrains/<station>/<travelDate>/<travelTime>')
def getAllTrains(station, travelDate, travelTime):
    travelTime = re.sub(r'\+', ' ', travelTime)
    travelDate = re.sub(r'\+', '/', travelDate)

    print(travelTime)
    print(travelDate)

    api = sle.getAllTrains(station, travelDate, travelTime)
    if not api["error"]:
        return Response(json.dumps(api), content_type="application/json"), 200
    else:
        return Response(json.dumps(api), content_type="application/json"), 400

if __name__ == '__main__':
    app.run()