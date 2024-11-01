from flask import Flask, Response, request
import json
import api
import fares
import time
import mistune

VERSION = json.loads(open("config.json").read())["VERSION"]

app = Flask(__name__)

def jsonHelper(jsn, status:int):
    return Response(json.dumps(jsn), content_type="application/json"), status

def parseStation(unparsed):
    unparsed = unparsed.split("-")
    station = ""

    for word in unparsed:
        station += word.lower().capitalize() + " "
    return station.strip()

def strToBoolHelper(string):
    if string in ["true", "True"]:
        return True
    if string in ["false", "False"]:
        return False
    return None

@app.route('/')
def home():
    return mistune.html(open("DOCS.md").read())

@app.route(f'/api/{VERSION}/stations/convertIDToStation/<id>')
def idToStn(id):
    translation = api.translateIDtoStation(id)
    if translation == None:
        return jsonHelper({"success": False, "message": "Invalid station ID"}, 400)
    return jsonHelper({"success": True, "stationName": translation}, 200)

@app.route(f'/api/{VERSION}/stations/convertStationToID/<name>')
def stnToid(name):
    name = parseStation(name)
    translation = api.translateStationToId(name)
    if translation == None:
        return jsonHelper({"success": False, "message": "Invalid station name"}, 400)
    return jsonHelper({"success": True, "stationID": translation}, 200)

@app.route(f'/api/{VERSION}/stations/listAllStations')
def listAllStn():
    return jsonHelper(api.getStations(), 200)


@app.route(f'/api/{VERSION}/trains/getStationByID/<id>')
def stationByID(id):
    stn = api.translateIDtoStation(id)
    if stn == None:
        return jsonHelper({"success": False, "message": "Invalid ID"}, 400)
    return jsonHelper(api.getAllTrainsAtStation(round(time.time()), stn, False), 200)

@app.route(f'/api/{VERSION}/trains/getStationByName/<name>')
def stationByName(name):
    # assuming the name is in the format "new-haven-union-station"
    # following converts it into New Haven Union Station
    station = parseStation(name)

    data = api.getAllTrainsAtStation(round(time.time()), station, False)
    if data == None:
        return jsonHelper({"success": False, "message": "Invalid name"}, 400)

    return jsonHelper(data, 200)

@app.route(f'/api/{VERSION}/fares/getRideFare', methods=["POST"])
def getFare():
    # user needs to POST:
    # - Ticket Type
    # - Is it off peak?
    # - Are they a senior?
    # - To
    # - From
    start = request.form.get("start")
    end = request.form.get("end")
    ticketType = request.form.get("ticketType")
    isSenior = request.form.get("isSenior")
    isOffPeak = request.form.get("isOffPeak")

    if start is None or end is None or ticketType is None or isSenior is None or isOffPeak is None:
        return jsonHelper({"success": False, "message": "Missing one or more parameter(s)"}, 400)

    result = fares.calculateFare(ticketType, isSenior, isOffPeak, start, end)
    if result == None:
        return jsonHelper({"success": False, "message": "Something went wrong"}, status=400)
    
    # add senior discount warning, per website
    if isSenior == "true" or isSenior == True:
        result["message"] = "Please note that reduced fares are not accepted on board weekday morning Peak trains. Please refer to the current schedule (https://shorelineeast.com/schedules) for Peak versus Off-Peak travel times."
    
    if isOffPeak == "true" or isOffPeak == True:
        result["message"] = "Please note that off peak fares only apply to trips that involve Metro North, which this API does not support. Setting this value to true or false will not impact the fare cost."
    
    return jsonHelper(result, status=200)

# if __name__ == '__main__':
#     app.run(debug=False, port=10394)