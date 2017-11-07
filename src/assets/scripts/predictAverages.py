#!/usr/bin/env python3
import MySQLdb
import collections
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

def getConnection():
    return MySQLdb.connect(host="localhost",
                         user="develop",
                         passwd="password",
                         db="parking_data")

def insertPredictionValues(db, lotName, percent):
    cur = db.cursor()
    query = "insert into " + lotName + "Prediction (intrvl, percentFilled) values (%s,%s)"
    arguments = (0, percent)
    cur.execute(query, arguments)
    db.commit();

def dropOldPredictions(db, lotName):
    cur = db.cursor()
    query = "delete from " + lotName + "Prediction"
    cur.execute(query)
    db.commit();

def getLotNamesAndSize():
    try:
        db = getConnection()
        cur = db.cursor()
        cur.execute("select * from lots")
        dic = collections.OrderedDict()
        for row in cur:
            dic[row[0]] = row[1]
        return dic
    except MySQLdb.Error as e:
        errorArray = []
        errorDic = collections.OrderedDict()
        errorDic["errors"] = str(e)
        errorArray.append(str(e))
        print("mySQL Query Error: ", e)
        return errorArray

def makePredictions(lotName, size):
    # Lot to make preditions for
    parkinglotName = lotName
    totalSpaces = size

    # Predictions time range and step interval
    beginTime = "09:00:00"
    endTime = "21:00:00"
    intervalMinutes = 15

    # Predictions output containers
    totalIntervals = 343;
    intervalsPerDay = 49
    allValues = [[] for x in range(totalIntervals)]
    averages = []
    finalPredictions = []

    # Format query
    queryString = 'select timestamp, freeSpots from {0};'.format(parkinglotName + "data")

    # Read data from DB
    fullDF = pd.read_sql((queryString),getConnection(),parse_dates=['timestamp'],index_col=['timestamp'])

    # Get free spot data
    df = fullDF['freeSpots']

    # Get all unique days
    days = pd.Series(df.index).map(pd.Timestamp.date).unique()

    # iterates over every day in series
    for day in days:
        # Get current day date string
        currentDayString = str(day)

        # Set start and end ranges
        begin = pd.to_datetime(currentDayString + " " + beginTime)
        end = pd.to_datetime(currentDayString + " " + endTime)
        current = begin

        # Get weekday integer mon = 0 sun = 6
        weekdayInt = begin.weekday()

        # Iterates over every interval in current day
        currentIntervalInt = 0
        while current <= end:
            closestValue = df.iloc[df.index.get_loc(current, method='nearest')]
            allValues[weekdayInt * intervalsPerDay + currentIntervalInt].append(closestValue)

            # Increment to next 15 minute interval
            current = current + timedelta(minutes=intervalMinutes)
            currentIntervalInt += 1

    # finds averages of each interval
    for intrvl in allValues:
        size = len(intrvl)
        if size > 0:
            total = 0
            for val in intrvl:
                total += val
            avg = total / size
            averages.append(avg)
        else:
            averages.append(0)

    # Calculate percent filled
    for val in averages:
        finalPredictions.append((totalSpaces - val) / totalSpaces)

    # Get db connection
    db = getConnection()

    # Drop old predictions
    dropOldPredictions(db, parkinglotName)

    # Insert new predictions
    for val in finalPredictions:
        insertPredictionValues(db, parkinglotName, val)

    # # iterates through series
    # i = 0
    # for freeSpots in df:
    #     timestamp = df.index[i]
    #     spotsLeft = freeSpots
    #
    #     print(timestamp, spotsLeft)
    #
    #     i += 1

# make predictions for all lots
lotDic = getLotNamesAndSize()
for name, size in lotDic.items() :
    try:
        makePredictions(name, size)
    except Exception as e:
        print(e)
