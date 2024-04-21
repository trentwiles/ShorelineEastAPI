from flask import Flask, Response
import json
import api
import stationapi

app = Flask(__name__)

def jsonHelper(jsn, status:int):
    return Response(json.dumps(jsn), content_type="application/json"), status

@app.route('/')
def home():
    return jsonHelper({"online": True}, 200)

@app.route('/api/v1/trains/stationByID')
def stationByID():
    return

@app.route('/api/v1/trains/stationByName')
def stationByName():
    return

if __name__ == '__main__':
    app.run(debug=True)