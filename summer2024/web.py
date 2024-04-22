from flask import Flask, Response, request
import json
import api
import stationapi
import time

app = Flask(__name__)

def jsonHelper(jsn, status:int):
    return Response(json.dumps(jsn), content_type="application/json"), status

def parseStation(unparsed):
    unparsed = unparsed.split("-")
    station = ""

    for word in unparsed:
        station += word.lower().capitalize() + " "
    return station.strip()

@app.route('/')
def home():
    return jsonHelper({"online": True}, 200)

@app.route('/api/v1/stations/convertIDToStation/<id>')
def idToStn(id):
    translation = api.translateIDtoStation(id)
    if translation == None:
        return jsonHelper({"success": False, "message": "Invalid station ID"}, 400)
    return jsonHelper({"success": True, "stationName": translation}, 200)

@app.route('/api/v1/stations/convertStationToID/<name>')
def stnToid(name):
    name = parseStation(name)
    translation = api.translateStationToId(name)
    if translation == None:
        return jsonHelper({"success": False, "message": "Invalid station name"}, 400)
    return jsonHelper({"success": True, "stationID": translation}, 200)

@app.route('/api/v1/stations/listAllStations')
def listAllStn():
    return jsonHelper(api.getStations(), 200)


@app.route('/api/v1/trains/getStationByID/<id>')
def stationByID(id):
    stn = api.translateIDtoStation(id)
    if stn == None:
        return jsonHelper({"success": False, "message": "Invalid ID"}, 400)
    return jsonHelper(api.getAllTrainsAtStation(round(time.time()), stn, False), 200)

@app.route('/api/v1/trains/getStationByName/<name>')
def stationByName(name):
    # assuming the name is in the format "new-haven-union-station"
    # following converts it into New Haven Union Station
    station = parseStation(name)

    data = api.getAllTrainsAtStation(round(time.time()), station, False)
    if data == None:
        return jsonHelper({"success": False, "message": "Invalid name"}, 400)

    return jsonHelper(data, 200)

if __name__ == '__main__':
    app.run(debug=True, port=10394)