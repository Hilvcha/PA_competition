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
    train_2.columns = ['TIME_GAP']
    test_2.columns = ['TIME_GAP']

    train_data = pd.merge(train_data, train_2, left_index=True, right_index=True)
    test_data = pd.merge(test_data, test_2, left_index=True, right_index=True)

    return train_data,test_data
