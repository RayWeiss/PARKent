#!/usr/bin/env python3
import MySQLdb
import collections
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA

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

    # Hour range to pull data from predicitons
    beginTime = "09:00:00"
    endTime = "21:00:00"

    # Day range to pull data from predicitons
    beginDay = "2017-10-02"
    endDay = "2017-10-08"

    # Days to sample for predictions (+1 day, and hours adjusted to limit NaN values)
    start = datetime(2017,10,1,0,0,0)
    end = datetime(2017,10,8,23,59,59)

    # Convert to parameters for query
    startParam = '\"{0}\"'.format(str(start))
    endParam = '\"{0}\"'.format(str(end))

    # Format query
    queryString = 'select timestamp, freeSpots from {0} where timestamp between {1} and {2};'.format(parkinglotName + "data",startParam,endParam)

    # Read data from DB
    data = pd.read_sql((queryString),getConnection(),parse_dates=['timestamp'],index_col=['timestamp'])

    # Get free spot data
    weekData = data['freeSpots']

    # Decompose data
    decomposition = seasonal_decompose(weekData, freq=288)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # Perform stats on data to make more stationary
    residual_cbrt = np.cbrt(residual)
    residual_cbrt.dropna(inplace=True)

    # Predict off of data
    # Get ARIMA model, fit results
    arima_model = ARIMA(residual_cbrt, order=(2, 1, 2))
    arima_results = arima_model.fit(disp=-1)

    # Convert to timeseries
    prediction_series = pd.Series(arima_results.fittedvalues, copy=True)

    # Get cummulative summation
    prediction_series_cumsum = prediction_series.cumsum()

    # Set index and add back cummulative summation, fill empty values with 0
    prediction_series_cbrt = pd.Series(residual_cbrt.ix[0], index=residual_cbrt.index)
    prediction_series_cbrt = prediction_series_cbrt.add(prediction_series_cumsum,fill_value=0)

    # Calculate the exponential of all elements in the input array. (unused)
    exponentials = np.exp(prediction_series_cbrt)

    # Reverse previous transformations for final prediction
    final_prediction = (np.power(prediction_series_cbrt, 3) + trend + seasonal)

    # # Plot data
    # plt.plot(weekData)
    # plt.plot(final_prediction)
    # # plt.plot(final_prediction - 23)
    # plt.show()

    # Set start and end ranges
    beginDatetime = pd.to_datetime(beginDay + " " + beginTime)
    endDatetime = pd.to_datetime(endDay + " " + endTime)
    currentDatetime = beginDatetime
    todayEndDatetime = pd.to_datetime(currentDatetime.strftime("%Y-%m-%d") + " " + endTime)

    # Get DB connection
    db = getConnection()

    # Drop old predictions
    dropOldPredictions(db, parkinglotName)

    # Insert new predictions
    while currentDatetime <= endDatetime:
        while currentDatetime <= todayEndDatetime:
            # Get closest value to current interval
            closestValue = final_prediction.iloc[final_prediction.index.get_loc(currentDatetime, method='nearest')]
            # Check if value is not a number
            if np.isnan(closestValue):
                closestValue = 0

            # Calculate percent filled
            percentFilled = (totalSpaces - closestValue) / totalSpaces

            # Handle bad values
            if percentFilled < 0:
                percentFilled = 0
            if percentFilled > 1:
                percentFilled = 1

            # Insert final result into DB
            insertPredictionValues(db, parkinglotName, percentFilled)

            # Increment to next 15 minute interval
            currentDatetime = currentDatetime + timedelta(minutes=15)

        # Increment to next day
        currentDatetime = currentDatetime + timedelta(days=1)
        currentDatetime = pd.to_datetime(currentDatetime.strftime("%Y-%m-%d") + " " + beginTime)
        todayEndDatetime = pd.to_datetime(currentDatetime.strftime("%Y-%m-%d") + " " + endTime)


# make predictions for all lots
lotDic = getLotNamesAndSize()
for name, size in lotDic.items() :
    try:
        makePredictions(name, size)
    except Exception as e:
        print(e)
