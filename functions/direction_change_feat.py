import pandas as pd
from utils.feature_utils import fun_direction, fun_direction_none


def rxd_direction_change_feat(train, test):
    train_1 = train[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction_none)
    test_1 = test[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction_none)
    train_1 = train_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    test_1 = test_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    train_1.rename(columns={'DIRECTION': 'DIRECTION_NONE'}, inplace=True)
    test_1.rename(columns={'DIRECTION': 'DIRECTION_NONE'}, inplace=True)
    # 删除包含有方向为-1的行
    ex_list = list(train.DIRECTION)
    ex_list.remove(-1)
    train_data = train[train.DIRECTION.isin(ex_list)]
    test_data = test[test.DIRECTION.isin(ex_list)]

    train_data = train_data[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction)
    test_data = test_data[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction)
    train_data = train_data[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    test_data = test_data[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO').mean()
    train_data = pd.merge(train_data, train_1, left_index=True,right_index=True)
    test_data = pd.merge(test_data, test_1, left_index=True,right_index=True)
    return train_data, test_data
