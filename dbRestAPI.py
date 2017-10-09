#!/usr/local/bin/python3
from flask import Flask
from flask_cors import CORS
import MySQLdb
import collections
import json

app = Flask(__name__)
CORS(app)

def query(queryString):
    try:
        db = MySQLdb.connect(host="localhost",
                             user="develop",
                             passwd="password",
                             db="parking_data")

        cur = db.cursor()
        cur.execute(queryString)
        results = cur.fetchall()
        resultsArray = []
        rowCount = 0
        for result in results:
            itemCount = 0
            dic = collections.OrderedDict()
            for item in result:
                dic[itemCount] = str(item)
                itemCount += 1
            resultsArray.append(dic)
            rowCount += 1
        return json.dumps(resultsArray)
        # db.commit();
    except MySQLdb.Error as e:
        print("mySQL Query Error: ", e)

@app.route("/allLots")
def getAllLotNames():
    return query("select * from lots")

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
