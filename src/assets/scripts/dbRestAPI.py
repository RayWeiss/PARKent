#!/usr/bin/env python3
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

    except MySQLdb.Error as e:
        errorArray = []
        errorDic = collections.OrderedDict()
        errorDic["errors"] = str(e)
        errorArray.append(errorDic)
        print("mySQL Query Error: ", e)
        return json.dumps(errorArray)

def queryArray(queryString):
    try:
        db = MySQLdb.connect(host="localhost",
                             user="develop",
                             passwd="password",
                             db="parking_data")

        cur = db.cursor()
        cur.execute(queryString)
        arr = []
        for row in cur:
            arr.append("".join(row))
        return arr
    except MySQLdb.Error as e:
        errorArray = []
        errorDic = collections.OrderedDict()
        errorDic["errors"] = str(e)
        errorArray.append(str(e))
        print("mySQL Query Error: ", e)
        return errorArray

def getPercent(parkingLotName):
    db = MySQLdb.connect(host="localhost",
                         user="develop",
                         passwd="password",
                         db="parking_data")

    cur = db.cursor()
    cur.execute("SELECT((SELECT freeSpots FROM " + parkingLotName + "Data ORDER BY timestamp DESC LIMIT 1) / (SELECT totalSpots FROM lots WHERE name = \"" + parkingLotName + "\")) as percentLeft")
    results = cur.fetchall()
    for result in results:
        for item in result:
            return str(item)

def getSpotsLeft(parkingLotName):
    db = MySQLdb.connect(host="localhost",
                         user="develop",
                         passwd="password",
                         db="parking_data")

    cur = db.cursor()
    cur.execute("SELECT freeSpots FROM " + parkingLotName + "Data ORDER BY timestamp DESC LIMIT 1")
    results = cur.fetchall()
    for result in results:
        for item in result:
            return str(item)

def getTimestamp(parkingLotName):
    db = MySQLdb.connect(host="localhost",
                         user="develop",
                         passwd="password",
                         db="parking_data")

    cur = db.cursor()
    cur.execute("SELECT timestamp FROM " + parkingLotName + "Data ORDER BY timestamp DESC LIMIT 1")
    results = cur.fetchall()
    for result in results:
        for item in result:
            return str(item)

def getTotalSpots(parkingLotName):
    db = MySQLdb.connect(host="localhost",
                         user="develop",
                         passwd="password",
                         db="parking_data")

    cur = db.cursor()
    cur.execute("SELECT totalSpots FROM lots WHERE name = \"" + parkingLotName + "\"")
    results = cur.fetchall()
    for result in results:
        for item in result:
            return str(item)

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

@app.route("/allStatus")
def getAllStatus():
    lotsArr = queryArray("SELECT name FROM lots")
    dic = collections.OrderedDict()

    for lot in lotsArr:
        dic[lot] = str(getPercent(lot))
    result = []
    result.append(dic)

    return json.dumps(result)

@app.route("/allFullStatus")
def getAllFullStatus():
    lotsArr = queryArray("SELECT name FROM lots")
    dic = collections.OrderedDict()

    for lot in lotsArr:
        fullArr = []
        fullArr.append(str(getPercent(lot)))
        fullArr.append(str(getSpotsLeft(lot)))
        fullArr.append(str(getTotalSpots(lot)))
        fullArr.append(str(getTimestamp(lot)))
        dic[lot] = fullArr
    result = []
    result.append(dic)

    return json.dumps(result)

@app.route("/fracLeft")
def getFracLeft():
    lotsArr = queryArray("SELECT name FROM lots")
    dic = collections.OrderedDict()

    for lot in lotsArr:
        fracArr = []
        fracArr.append(str(getSpotsLeft(lot)))
        fracArr.append(str(getTotalSpots(lot)))
        dic[lot] = fracArr
    result = []
    result.append(dic)

    return json.dumps(result)

@app.route("/predictions/<parkingLotName>")
def getPredictionsFor(parkingLotName):
    return query("SELECT percentFilled FROM " + parkingLotName + "Prediction")

# Brandon's Stuff
####################################################################
host="localhost"
user="develop"
passwd="password"

@app.route("/lotNames")
def getLotNames():
	lotsArr = queryArray("SELECT name FROM lots")
	result = []
	result.append(lotsArr)

	return json.dumps(result)

@app.route("/addlot/<lotName>/<totalSpots>/<lat>/<lon>/<lotNum>")
def addLot(lotName, totalSpots, lat, lon, lotNum):
	try:
		db = MySQLdb.connect(host, user, passwd, db="parking_data")
		url = "https://streetsoncloud.com/parking/rest/occupancy/id/" + lotNum
		useQuery = "use parking_data;"
		query = "insert into lots values (\"" + lotName + "\"," + totalSpots + "," + lat + "," + lon + ",\"" + url + "\");"
		dataTable = "create table " + lotName + "Data (timeStamp TIMESTAMP NOT NULL, freeSpots INT(10) UNSIGNED NOT NULL, PRIMARY KEY (timeStamp));"
		predictTable = "create table " + lotName + "Prediction ( intrvl MEDIUMINT NOT NULL AUTO_INCREMENT, percentFilled DOUBLE(11,8) NOT NULL, PRIMARY KEY (intrvl) );"
		cur = db.cursor()
		cur.execute(useQuery)
		cur.execute(query)
		cur.execute(dataTable)
		cur.execute(predictTable)
		successJson = "{\"0\":\"true\"}"
		db.commit()
		db.close()
		return successJson

	except MySQLdb.Error as e:
		return returnError(e)

@app.route("/createdb/<dbName>/<lat>/<lon>")
def createDB(dbName, lat, lon):
	try:
		db = MySQLdb.connect(host, user, passwd)

		dbQuery = "create database " + dbName + ";"
		useQuery = "use " + dbName + ";"
		centerQuery = "create table center (lat double(10,8), lon double(10,8));"
		insertQuery = "insert into center values (" + lat + "," + lon + ");"
		lotsTable = "CREATE TABLE lots(name VARCHAR(25) NOT NULL, totalSpots int(10) UNSIGNED NOT NULL, lat DOUBLE(10,8) NOT NULL, lon DOUBLE(11,8) NOT NULL, url VARCHAR(200) NOT NULL, PRIMARY KEY(name));"
		cur = db.cursor()
		cur.execute(dbQuery)
		cur.execute(useQuery)
		cur.execute(centerQuery)
		cur.execute(insertQuery)
		cur.execute(lotsTable)
		successJson = "{\"0\":\"true\"}"
		db.commit()
		db.close()
		return successJson

	except MySQLdb.Error as e:
		return returnError(e)

@app.route("/dropdb/<dbName>")
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

@app.route("/removelot/<lotName>")
def dropLot( lotName):
	try:
		db = MySQLdb.connect(host, user, passwd, db="parking_data")
		cur = db.cursor()
		useQuery = "use parking_data;"
		dropDataQuery = "drop table " + lotName + "Data;"
		dropPredictionQuery = "drop table " + lotName + "Prediction;"
		removeFromLots = "delete from lots where name = \""+ lotName + "\";"

		print(removeFromLots)
		cur.execute(useQuery)
		cur.execute(removeFromLots)
		cur.execute(dropDataQuery)
		cur.execute(dropPredictionQuery)
		successJson = "{\"0\":\"true\"}"
		db.commit()
		db.close()
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

@app.route("/databases")
def returnDatabases():
	try:
		db = MySQLdb.connect(host,
			user,
			passwd)

		cur = db.cursor()
		databaseArr = queryArray("show databases like '%parking%';")
		result = []
		result.append(databaseArr)
		return json.dumps(result)

	except MySQLdb.Error as e:
		return returnError(e)

if __name__ == "__main__":
    # local
    app.run()
    # remote
    # app.run(host='0.0.0.0',port='5000')
