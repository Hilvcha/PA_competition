# coding: utf-8
# created by rxd
import pandas as pd
import math
from utils.feature_utils import fun_direction, fun_direction_none


def time_gap_direction_change_feat(train, test):
    # 取方向缺失次数
    train_1 = train[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                    as_index=False).agg(fun_direction_none)
    test_1 = test[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                  as_index=False).agg(fun_direction_none)
    train_1 = train_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    test_1 = test_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    train_1.rename(columns={'DIRECTION': 'DIRECTION_NONE'}, inplace=True)
    test_1.rename(columns={'DIRECTION': 'DIRECTION_NONE'}, inplace=True)

    # 删除包含有方向为-1的行
    ex_list = list(train.DIRECTION)
    ex_list.remove(-1)
    train_data = train[train.DIRECTION.isin(ex_list)]
    test_data = test[test.DIRECTION.isin(ex_list)]

    # 方向变化方差
    train_data = train_data[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                            as_index=False).agg(
        fun_direction)
    test_data = test_data[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                          as_index=False).agg(
        fun_direction)
    train_data = train_data[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    test_data = test_data[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()

    train_data.rename(columns={'DIRECTION': 'DIRECTION_VAR'}, inplace=True)
    test_data.rename(columns={'DIRECTION': 'DIRECTION_VAR'}, inplace=True)

    train_data = pd.merge(train_data, train_1, left_index=True, right_index=True)
    test_data = pd.merge(test_data, test_1, left_index=True, right_index=True)

    # 取组内时间差距
    train_2 = train[['TERMINALNO', 'TRIP_ID', 'TIME_STAMP']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                     as_index=False).agg(
        lambda arr: arr.iloc[-1] - arr.iloc[0])
    test_2 = test[['TERMINALNO', 'TRIP_ID', 'TIME_STAMP']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                   as_index=False).agg(
        lambda arr: arr.iloc[-1] - arr.iloc[0])

    train_2 = train_2[['TERMINALNO', 'TIME_STAMP']].groupby(['TERMINALNO']).mean()
    test_2 = test_2[['TERMINALNO', 'TIME_STAMP']].groupby(['TERMINALNO']).mean()

    train_data = pd.merge(train_data, train_2, left_index=True, right_index=True)
    test_data = pd.merge(test_data, test_2, left_index=True, right_index=True)

    # 加入了危险系数
    train_direction_risk = train[["TERMINALNO", 'TRIP_ID', 'DIRECTION', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                          as_index=False).apply(
        direction_risk)

    train_direction_risk = train_direction_risk[["TERMINALNO", 'TRIP_ID', 'DIRECTION_RISK']].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).mean()

    train_direction_risk = train_direction_risk[["TERMINALNO", 'DIRECTION_RISK']].groupby(["TERMINALNO"],
                                                                                          as_index=True).mean()

    train_data = pd.merge(test_data, train_direction_risk, left_index=True, right_index=True)


    test_direction_risk = test[["TERMINALNO", 'TRIP_ID', 'DIRECTION', 'SPEED']].groupby(["TERMINALNO", 'TRIP_ID'],
                                                                                          as_index=False).apply(
        direction_risk)

    test_direction_risk = test_direction_risk[["TERMINALNO", 'TRIP_ID', 'DIRECTION_RISK']].groupby(
        ["TERMINALNO", 'TRIP_ID'],
        as_index=False).mean()

    test_direction_risk = test_direction_risk[["TERMINALNO", 'DIRECTION_RISK']].groupby(["TERMINALNO"],
                                                                                          as_index=True).mean()

    test_data = pd.merge(test_data, test_direction_risk, left_index=True, right_index=True)
    return train_data, test_data


def direction_risk(arr):
    tempdirection = arr['DIRECTION'].iloc[0]
    tempspeed = arr['SPEED'].iloc[0]
    dir_risk = 0

    for index, row in arr.iterrows():
        D_direction = min(abs(row["DIRECTION"] - tempdirection), abs(360 + tempdirection - row["DIRECTION"])) / 90.0
        D_speed = abs(row['SPEED'] - tempspeed)
        dir_risk += math.pow(D_speed / 10, D_direction / 100)
        tempspeed = row['SPEED']
        tempdirection = row['DIRECTION']
        arr['DIRECTION_RISK'] = dir_risk
    return arr
