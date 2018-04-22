# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from utils.feature_utils import df_empty


# TERMINALNO,TIME,TRIP_ID,LONGITUDE,LATITUDE,DIRECTION,HEIGHT,SPEED,CALLSTATE,Y
# 对传入的表按trip_id分组，取每组的海拔的最大连续子数组，对每个人的所有行程的子数组取最大，平均, 方差。
# def max_sub(arr):
#     sum = 0
#     height = -999
#     tempheight = arr.iloc[0]
#     for h in arr:
#         sum += h - tempheight
#         if sum > height:
#             height = sum
#         if sum < 0:
#             sum = 0
#         tempheight = h
#     arr['secc_inc']=sum
#     return arr


def speed_risk(arr):
    # 上坡的最大子数组
    sum = 0
    height = -999

    tempheight = arr['HEIGHT'].iloc[0]
    tempdirection = arr['DIRECTION'].iloc[0]
    tempspeed = arr['SPEED'].iloc[0]
    # 海拔变化危险系数
    height_risk = 0
    # 方向变化危险系数
    dir_risk = 0
    # 通话危险系数
    call_risk = 0
    for index, row in arr.iterrows():
        sum += row['HEIGHT'] - tempheight
        if sum > height:
            height = sum
        if sum < 0:
            sum = 0
        # 如果具有速度，且在打电话
        if tempspeed > 0 and row["CALLSTATE"] != 4:
            if row["CALLSTATE"] == 0:
                call_risk += math.exp(tempspeed / 10) * 0.02
            else:
                call_risk += math.exp(tempspeed / 10)

        D_height = abs(row['HEIGHT'] - tempheight)

        if row['SPEED']==-1:
            D_speed=0
        else:
            D_speed = abs(row['SPEED'] - tempspeed)

        height_risk += math.pow(D_speed / 10, D_height / 100)

        if row['SPEED'] == -1:
            pass
        else:
            tempspeed = row['SPEED']

        tempheight = row['HEIGHT']
        if row['DIRECTION'] == -1:
            pass
        else:
            D_direction = min(abs(row["DIRECTION"] - tempdirection), abs(360 + tempdirection - row["DIRECTION"])) / 90.0
            dir_risk += math.pow(D_speed, D_direction/10)

            tempdirection = row['DIRECTION']

    arr['SUCC_INC'] = height
    arr["CALLSTATE_RISK"] = call_risk
    arr['HEIGHT_RISK'] = height_risk
    arr['DIRECTION_RISK'] = dir_risk

    return arr

def height_feet(data):

    # 加入了危险系数
    data_speed_risk = data[["TERMINALNO", 'TRIP_ID', 'HEIGHT', 'SPEED', 'DIRECTION', "CALLSTATE"]].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).apply(
        speed_risk)
    # 为tripid聚合
    data_speed_risk = data_speed_risk[
        ["TERMINALNO", 'TRIP_ID', 'HEIGHT_RISK', 'DIRECTION_RISK', 'SUCC_INC', "CALLSTATE_RISK"]].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).mean()
    max_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).max()
    mean_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).mean()
    var_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).var()
    train_data=pd.concat([max_data, mean_data, var_data], axis=1)
    train_data.columns = ['MAX_SUCC_INC', 'MEAN_SUCC_INC', 'VAR_SUCC_INC']

    data_speed_risk = data_speed_risk[["TERMINALNO", 'HEIGHT_RISK', 'DIRECTION_RISK', "CALLSTATE_RISK"]].groupby(
        ["TERMINALNO"],
        as_index=True).sum()
    train_data=pd.concat([train_data,  data_speed_risk], axis=1)


    return train_data

    # # 加入了危险系数
    # train_direction_risk = train[["TERMINALNO", 'TRIP_ID', 'DIRECTION', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
    #                                                                                       as_index=False).apply(
    #     direction_risk)
    #
    # train_direction_risk = train_direction_risk[["TERMINALNO", 'TRIP_ID', 'DIRECTION_RISK']].groupby(
    #     ["TERMINALNO", 'TRIP_ID'],
    #     as_index=False).mean()
    #
    # train_direction_risk = train_direction_risk[["TERMINALNO", 'DIRECTION_RISK']].groupby(["TERMINALNO"],
    #                                                                                       as_index=True).mean()
    #
    # train_data = pd.merge(train_data, train_direction_risk, left_index=True, right_index=True)
    #
    # test_direction_risk = test[["TERMINALNO", 'TRIP_ID', 'DIRECTION', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
    #                                                                                     as_index=False).apply(
    #     direction_risk)
    #
    # test_direction_risk = test_direction_risk[["TERMINALNO", 'TRIP_ID', 'DIRECTION_RISK']].groupby(
    #     ["TERMINALNO", 'TRIP_ID'],
    #     as_index=False).mean()
    #
    # test_direction_risk = test_direction_risk[["TERMINALNO", 'DIRECTION_RISK']].groupby(["TERMINALNO"],
    #                                                                                     as_index=True).mean()
    #
    # test_data = pd.merge(test_data, test_direction_risk, left_index=True, right_index=True)
