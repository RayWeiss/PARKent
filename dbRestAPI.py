#!/usr/local/bin/python3
from flask import Flask
from flask_cors import CORS
import MySQLdb
import collections
import json
import dbProcedures

app = Flask(__name__)
CORS(app)


#DATABASE CREDENTIALS
host="localhost"
user="root"
passwd="root"

def query(queryString):
	try:
		db = MySQLdb.connect(host, user, passwd, db="parking_data")

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

@app.route("/addlot/<lotName>/<totalSpots>/<lat>/<lon>/<url>")
def addLot(lotName, totalSpots, lat, lon, url):
	try:
		db = MySQLdb.connect(host, user, passwd, db="parking_data")

		useQuery = "use parking_data;"
		query = "insert into lots values (\"" + lotName + "\"," + totalSpots + "," + lat + "," + lon + ",\"" + url + "\");"
		dataTable = "create table " + lotName + "Data ( timeStamp TIMESTAMP NOT NULL, freeSpots INT(10) UNSIGNED NOT NULL, PRIMARY KEY (timeStamp));" 
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
		cur = db.cursor()
		cur.execute(dbQuery)
		cur.execute(useQuery)
		cur.execute(centerQuery)
		cur.execute(insertQuery)
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

def queryArray(queryString):
    try:
        db = MySQLdb.connect(host, user, passwd, db="parking_data")
        cur = db.cursor()
        cur.execute(queryString)
        arr = []
        for row in cur:
            arr.append("".join(row))
        return arr
    except MySQLdb.Error as e:
        return returnError(e)

@app.route("/lotNames")
def getAllStatus():
    lotsArr = queryArray("SELECT name FROM lots")
    result = []
    result.append(lotsArr)

    return json.dumps(result)

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
