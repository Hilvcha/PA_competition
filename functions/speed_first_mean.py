# coding : utf-8
from utils import data_utils
import numpy as np

# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

def wyj_speed_first_mean(train, test):
    train_data=train[['TERMINALNO','TRIP_ID','SPEED']].groupby(['TERMINALNO','TRIP_ID'],as_index=False).mean()

    train_data=train_data[['TERMINALNO','SPEED']].groupby(['TERMINALNO']).agg(lambda arr: arr.iloc[0])

    test_data = test[['TERMINALNO', 'TRIP_ID', 'SPEED']].groupby(['TERMINALNO', 'TRIP_ID'],as_index=False).mean()
    test_data = test_data[['TERMINALNO', 'SPEED']].groupby(['TERMINALNO']).agg(lambda arr: arr.iloc[0])

    return train_data,test_data
