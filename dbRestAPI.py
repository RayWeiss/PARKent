#!/usr/local/bin/python3
from flask import Flask
from flask_cors import CORS
import MySQLdb
import collections
import json

app = Flask(__name__)
CORS(app)


#DATABASE CREDENTIALS
host="localhost"
user="root"
passwd="root"

def query(queryString):
    try:
        db = MySQLdb.connect(host,
                             user,
                             passwd,
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
        return returnError(e)

def addLot(lotName, totalSpots, lat, lon, url):
        try:
                db = MySQLdb.connect(host,
                             user,
                             passwd,
                             db="parking_data")


                query = "Call add_lot (\"" + lotName + "\"," + totalSpots + "," + lat + "," + lon + ",\"" + url + "\");"
                cur = db.cursor()
                cur.execute(query)
                successJson = "{\"0\":\"true\"}"
                return successJson

        except MySQLdb.Error as e:
            return returnError(e)



def createDB(dbName):
        try:
                db = MySQLdb.connect(host,
                             user,
                             passwd)

                dbQuery = "create database " + dbName + ";"
                useQuery = "use " + dbName + ";"
                centerQuery = "create table center (lat double(10,8), lon double(10,8));"

                cur = db.cursor()
                cur.execute(dbQuery)
                cur.execute(useQuery)
                cur.execute(centerQuery)
                successJson = "{\"0\":\"true\"}"
                return successJson

        except MySQLdb.Error as e:
            return returnError(e)


def addCenter(dbName, lat, lon):
        try:
                db = MySQLdb.connect(host,
                             user,
                             passwd)

                cur = db.cursor()
                useQuery = "use " + dbName + ";"
                insertQuery = "insert into center (lat, lon) values(" + lat + "," + lon + ");"
                print (useQuery)
                cur.execute(useQuery)
                cur.execute(insertQuery)
                successJson = "{\"0\":\"true\"}"
                return successJson

        except MySQLdb.Error as e:
            return returnError(e)

def removeDB(dbName):
        try:
                db = MySQLdb.connect(host,
                             user,
                             passwd)

                cur = db.cursor()
                dropQuery = "drop database " + dbName + ";"
                cur.execute(dropQuery)
                successJson = "{\"0\":\"true\"}"
                return successJson

        except MySQLdb.Error as e:
            return returnError(e)

def dropLot(dbName, lotName):
        try:
                db = MySQLdb.connect(host,
                             user,
                             passwd) 
                cur = db.cursor()
                useQuery = "use " + dbName + ";"
                dropDataQuery = "drop table " + lotName + "Data;"
                dropPredictionQuery = "drop table " + lotName + "Prediction;"
                removeFromLots = "Call remove_from_lots (\"" + lotName + "\");"
                
                print(removeFromLots)
                cur.execute(useQuery)
                cur.execute(removeFromLots)
                cur.execute(dropDataQuery)
                cur.execute(dropPredictionQuery)
                #cur.execute(removeFromLots)
                successJson = "{\"0\":\"true\"}"
                return successJson

        except MySQLdb.Error as e:
            return returnError(e)

def returnError(e):
                errorArray = []
                errorDic = collections.OrderedDict()
                errorDic["errors"] = str(e)
                errorArray.append(errorDic)
                print("mySQL Query Error: ", e)
                return json.dumps(errorArray)



@app.route("/addlot/<lotName>/<totalSpots>/<lat>/<lon>/<url>")
def addNewLot(lotName, totalSpots, lat, lon, url):
        return addLot(lotName, totalSpots, lat, lon, url)

@app.route("/removelot/<dbName>/<lotName>")
def removeLot(dbName, lotName):
	return dropLot(dbName, lotName)

@app.route("/createdb/<dbName>/<lat>/<lon>")
def createDatabase(dbName, lat, lon):
	createDB(dbName)
	return addCenter(dbName, lat,lon)

@app.route("/dropdb/<dbName>")
def dropDB(dbName):
	return removeDB(dbName)

@app.route("/allLots")
def getAllLotInfo():
    return query("SELECT * FROM lots")

@app.route("/spotsleft/<parkingLotName>")
def getAvailableSpotsFor(parkingLotName):
    return query("SELECT freeSpots FROM " + parkingLotName + "Data ORDER BY timestamp DESC LIMIT 1")

@app.route("/percentleft/<parkingLotName>")
def getPercentLeftFor(parkingLotName):
    return query("SELECT((SELECT freeSpots FROM " + parkingLotName + "Data ORDER BY timestamp DESC LIMIT 1) / (SELECT totalSpots FROM lots WHERE name = \"" + parkingLotName + "\")) as percentLeft")

@app.route("/prediction/<parkingLotName>")
def getPredictionFor(parkingLotName):
    # query DB for parkingLotName prediction
    return parkingLotName + " .0 .03 .07 .20 .25 .4 .5 .9 1.0 1.0 1.0 .8 .9 1.0"


if __name__ == "__main__":
    app.run()