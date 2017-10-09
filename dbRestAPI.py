#!/usr/local/bin/python3
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)



@app.route("/allLots")
def getAllLotNames():
    # query DB for all lot names
    return "lot 1, lot 2 lot 3"

@app.route("/spotsleft/<parkingLotName>")
def getAvailableSpotsFor(parkingLotName):
    # query DB for parkingLotName spots left
    return parkingLotName + " 100"

@app.route("/prediction/<parkingLotName>")
def getPredictionFor(parkingLotName):
    # query DB for parkingLotName prediction
    return parkingLotName + " .0 .03 .07 .20 .25 .4 .5 .9 1.0 1.0 1.0 .8 .9 1.0"


if __name__ == "__main__":
    app.run()
