# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from utils.feature_utils import df_empty


# TERMINALNO,TIME,TRIP_ID,LONGITUDE,LATITUDE,DIRECTION,HEIGHT,SPEED,CALLSTATE,Y
# 对传入的表按trip_id分组，取每组的海拔的最大连续子数组，对每个人的所有行程的子数组取最大，平均, 方差。
def max_sub(arr):
    sum = 0
    height = -999
    tempheight = arr.iloc[0]
    for h in arr:
        sum += h - tempheight
        if sum > height:
            height = sum
        if sum < 0:
            sum = 0
        tempheight = h
    return sum


def speed_risk(arr):
    tempheight = arr['HEIGHT'].iloc[0]
    tempspeed = arr['SPEED'].iloc[0]
    height_risk = 0

    for index, row in arr.iterrows():
        D_height = abs(row['HEIGHT'] - tempheight)
        D_speed = abs(row['SPEED'] - tempspeed)
        height_risk += math.pow(D_speed / 10, D_height / 100)
        tempspeed = row['SPEED']
        tempheight = row['HEIGHT']
    arr['HEIGHT_RISK'] = height_risk
    return arr


def height_feet(train, test):
    train_data = train[["TERMINALNO", 'TRIP_ID', 'HEIGHT']].groupby(["TERMINALNO", 'TRIP_ID'], as_index=False).agg(
        max_sub)
    max_train = train_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).max()
    mean_train = train_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).mean()
    var_train = train_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).var()
    train_data = pd.merge(max_train, mean_train, left_index=True, right_index=True)
    train_data = pd.merge(train_data, var_train, left_index=True, right_index=True)

    train_data.columns = ['max_secc_inc', 'mean_secc_inc', 'var_secc_inc']

    test_data = test[["TERMINALNO", 'TRIP_ID', 'HEIGHT']].groupby(["TERMINALNO", 'TRIP_ID'], as_index=False).agg(
        max_sub)

    max_test = test_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).max()
    mean_test = test_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).mean()
    var_test = test_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).var()
    test_data = pd.merge(max_test, mean_test, left_index=True, right_index=True)
    test_data = pd.merge(test_data, var_test, left_index=True, right_index=True)

    test_data.columns = ['max_secc_inc', 'mean_secc_inc', 'var_secc_inc']

    # 加入了危险系数
    train_height_risk = train[["TERMINALNO", 'TRIP_ID', 'HEIGHT', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                    as_index=False).apply(
        speed_risk)

    train_height_risk = train_height_risk[["TERMINALNO", 'TRIP_ID', 'HEIGHT_RISK']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                            as_index=False).mean()

    train_height_risk = train_height_risk[["TERMINALNO",'HEIGHT_RISK']].groupby(["TERMINALNO"],
                                                                                            as_index=True).mean()
    train_data=pd.merge(train_data,train_height_risk,left_index=True, right_index=True)

    # test
    test_height_risk = test[["TERMINALNO", 'TRIP_ID', 'HEIGHT', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                    as_index=False).apply(
        speed_risk)

    test_height_risk = test_height_risk[["TERMINALNO", 'TRIP_ID', 'HEIGHT_RISK']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                            as_index=False).mean()

    test_height_risk = test_height_risk[["TERMINALNO", 'HEIGHT_RISK']].groupby(["TERMINALNO"],
                                                                                 as_index=True).mean()
    test_data = pd.merge(test_data, test_height_risk, left_index=True, right_index=True)
    return train_data, test_data
