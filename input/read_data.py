# coding : utf-8
import pandas as pd
from utils.feature_utils import time_reform
import time
import numpy as np

from functools import wraps


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{}:{} seconds'.format(func.__module__, func.__name__, round(end - start, 2)))
        return r

    return wrapper


@timethis
def read_data(train_path, test_path):
    # dtypes_train = {
    #     'TERMINALNO': 'int32',
    #     'TIME': 'int32',
    #     'TRIP_ID': 'int8',
    #     'LATITUDE': 'float32',
    #     'LONGITUDE': 'float32',
    #     'DIRECTION': 'int8',
    #     'HEIGHT': 'float32',
    #     'SPEED': 'float32',
    #     'CALLSTATE': 'int8',
    #     'Y': 'float32'
    # }
    # dtypes_test = {
    #     'TERMINALNO': 'int32',
    #     'TIME': 'int32',
    #     'TRIP_ID': 'int8',
    #     'LATITUDE': 'float32',
    #     'LONGITUDE': 'float32',
    #     'DIRECTION': 'int8',
    #     'HEIGHT': 'float32',
    #     'SPEED': 'float32',
    #     'CALLSTATE': 'int8',
    # }


    train = pd.read_csv(train_path, encoding='utf8')
    test = pd.read_csv(test_path, encoding='utf8')
    # train.replace(-1,np.nan,inplace=True)
    # test.replace(-1,np.nan,inplace=True)
    # train.interpolate(inplace=True)
    # test.interpolate(inplace=True)


    train=train[train['TERMINALNO'] <= (train['TERMINALNO'].max())]
    # # 将数据集中的时间戳转化为时间
    train['TIME1'] = pd.to_datetime(train.TIME.apply(time_reform), format='%Y-%m-%d %H:%M:%S')
    test['TIME1'] = pd.to_datetime(test.TIME.apply(time_reform), format='%Y-%m-%d %H:%M:%S')

    train.rename(columns={"TIME": "TIME_STAMP", "TIME1": "TIME"}, inplace=True)
    test.rename(columns={"TIME": "TIME_STAMP", "TIME1": "TIME"}, inplace=True)

    # 对数据按照时间顺序排序
    train.sort_values(by=['TERMINALNO', 'TIME'], inplace=True)
    test.sort_values(by=['TERMINALNO', 'TIME'], inplace=True)
    train.reset_index(drop=True, inplace=True)
    test.reset_index(drop=True, inplace=True)
    train[['TERMINALNO']]=train[['TERMINALNO']].astype(int)
    test[['TERMINALNO']]=test[['TERMINALNO']].astype(int)

    # train_user = train['TERMINALNO'].unique()
    # train_trip_idlist = []
    # for TERMINALNO in train_user:
    #     user_data = train.loc[train['TERMINALNO'] == TERMINALNO]
    #     trip_id = 1
    #     temptime = user_data['TIME_STAMP'].iloc[0]
    #     for index, row in user_data.iterrows():
    #         if row['TIME_STAMP'] - temptime <= 60:
    #             train_trip_idlist.append(trip_id)
    #         else:
    #             trip_id += 1
    #             train_trip_idlist.append(trip_id)
    #         temptime = row['TIME_STAMP']
    # train['TRIP_ID'] = train_trip_idlist
    #
    # # 对时间差超过一分钟的作为新的trip_id
    # test_user = test['TERMINALNO'].unique()
    # test_trip_idlist = []
    # for TERMINALNO in test_user:
    #     user_data = test.loc[test['TERMINALNO'] == TERMINALNO]
    #     trip_id = 1
    #     temptime = user_data['TIME_STAMP'].iloc[0]
    #     for index, row in user_data.iterrows():
    #         if row['TIME_STAMP'] - temptime <= 60:
    #             test_trip_idlist.append(trip_id)
    #         else:
    #             trip_id += 1
    #             test_trip_idlist.append(trip_id)
    #         temptime = row['TIME_STAMP']
    # test['TRIP_ID'] = test_trip_idlist

    # 删除只有一分钟记录的行程
    # train_data = train[['TERMINALNO', 'TRIP_ID', 'HEIGHT']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).count()
    # train_data = train_data[train_data['HEIGHT'] > 1]
    # del train_data['HEIGHT']
    # train = pd.merge(train_data, train, on=['TERMINALNO', 'TRIP_ID'], how='left', )

    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y
    #
    #     t=train[['TERMINALNO','TRIP_ID']].groupby('TERMINALNO').agg(lambda arr: arr.iloc[0])
    #     print(t)
    return train, test
