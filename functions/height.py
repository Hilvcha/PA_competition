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
    # sum = 0
    # height = -999

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
        # sum += row['HEIGHT'] - tempheight
        # if sum > height:
        #     height = sum
        # if sum < 0:
        #     sum = 0

        if tempspeed > 0 and row["CALLSTATE"] != 4:
            if row["CALLSTATE"] == 0:
                call_risk += math.exp(tempspeed / 10) * 0.02
            else:
                call_risk += math.exp(tempspeed / 10)

        D_height = abs(row['HEIGHT'] - tempheight)

        D_speed = abs(row['SPEED'] - tempspeed)

        height_risk += math.pow(row["SPEED"], D_height / 100)

        tempspeed = row['SPEED']

        tempheight = row['HEIGHT']

        D_direction = min(abs(row["DIRECTION"] - tempdirection), abs(360 + tempdirection - row["DIRECTION"])) / 90.0
        dir_risk += math.pow((row["SPEED"] / 10), D_direction / 10)

        tempdirection = row['DIRECTION']

    # arr['SUCC_INC'] = height
    arr["CALLSTATE"] = call_risk
    arr['HEIGHT'] = height_risk
    arr['DIRECTION'] = dir_risk

    return arr


def height_feet(data):
    # 加入了危险系数
    data_speed_risk = data[["TERMINALNO", 'TRIP_ID', 'HEIGHT', 'SPEED', 'DIRECTION', "CALLSTATE"]].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).apply(
        speed_risk)
    # 为tripid聚合
    data_speed_risk = data_speed_risk[
        ["TERMINALNO", 'TRIP_ID', 'HEIGHT', 'DIRECTION', "CALLSTATE"]].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).first()
    # max_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).max()
    # mean_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).mean()
    # var_data = data_speed_risk[["TERMINALNO", 'SUCC_INC']].groupby(["TERMINALNO"], as_index=True).var()
    # train_data=pd.concat([max_data, mean_data, var_data], axis=1)
    # train_data.columns = ['MAX_SUCC_INC', 'MEAN_SUCC_INC', 'VAR_SUCC_INC']

    train_data = data_speed_risk[["TERMINALNO", 'HEIGHT', 'DIRECTION', "CALLSTATE"]].groupby(
        ["TERMINALNO"],
        as_index=True).sum()
    # 时间统计特征
    height_sta = data[['TERMINALNO', "HEIGHT"]].groupby(['TERMINALNO']).agg([np.mean, np.var])
    # 最大行程时间
    max_time = data[['TERMINALNO', "TRIP_ID", "TIME"]].groupby(["TERMINALNO", 'TRIP_ID'], as_index=False).count()
    max_time = max_time[['TERMINALNO', 'TIME']].groupby(["TERMINALNO"]).max()
    # 速度统计特征
    speed_sta = data[['TERMINALNO', "SPEED"]].groupby(['TERMINALNO']).agg([np.mean, np.max])
    # # 平均下
    # height_down = data[['TERMINALNO', "TRIP_ID", "HEIGHT"]].groupby(["TERMINALNO", 'TRIP_ID'], as_index=False).agg(
    #     maxSubArray)
    # height_down = height_down[['TERMINALNO', "HEIGHT"]].groupby(['TERMINALNO']).agg([np.mean, np.min])
    # # 平均上坡
    # height_up = data[['TERMINALNO', "TRIP_ID", "HEIGHT"]].groupby(["TERMINALNO", 'TRIP_ID'], as_index=False).agg(
    #     minSubArray)
    # height_up = height_up[['TERMINALNO', "HEIGHT"]].groupby(['TERMINALNO']).agg([np.mean, np.max])

    train_data = pd.concat([train_data, height_sta, max_time, speed_sta,], axis=1)
    train_data.columns = ['height_risk', 'direction_risk', "callstate_risk", "height_mean", "height_var", "max_time",
                          "speed_mean", "speed_max",]

    return train_data


# 'TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
#                            'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'
def maxSubArray(arr):
    height = 99999
    sum = 0
    tempheight = arr.iloc[0]
    for h in arr:
        sum += h - tempheight
        if sum < height:
            height = sum
        if sum > 0:
            sum = 0
        tempheight = h
    return height

def minSubArray(arr):
    height = -99999
    sum = 0
    tempheight = arr.iloc[0]
    for h in arr:
        sum += h - tempheight
        if sum > height:
            height = sum
        if sum < 0:
            sum = 0
        tempheight = h
    return height
