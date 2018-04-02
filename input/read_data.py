# coding : utf-8
import pandas as pd
from utils.feature_utils import time_reform


def read_data(train_path, test_path):
    # dtypes_train = {
    #     'TERMINALNO': 'uint32',
    #    # 'TIME': 'uint64',
    #     'TRIP_ID': 'uint8',
    #     'LATITUDE': 'float32',
    #     'LONGITUDE': 'float32',
    #     'DIRECTION': 'uint8',
    #     'HEIGHT': 'float32',
    #     'SPEED': 'float32',
    #     'CALLSTATE': 'uint8',
    #     'Y': 'float32'
    # }
    # dtypes_test = {
    #     'TERMINALNO': 'uint32',
    #    # 'TIME': 'uint64',
    #     'TRIP_ID': 'uint8',
    #     'LATITUDE': 'float32',
    #     'LONGITUDE': 'float32',
    #     'DIRECTION': 'uint8',
    #     'HEIGHT': 'float32',
    #     'SPEED': 'float32',
    #     'CALLSTATE': 'uint8',
    # }
    train = pd.read_csv(train_path, encoding='utf8')
    test = pd.read_csv(test_path, encoding='utf8')

    # 将数据集中的时间戳转化为时间
    train.TIME = pd.to_datetime(train.TIME.apply(time_reform), format='%Y-%m-%d %H:%M:%S')
    test.TIME = pd.to_datetime(test.TIME.apply(time_reform), format='%Y-%m-%d %H:%M:%S')

    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y
    #
    #     t=train[['TERMINALNO','TRIP_ID']].groupby('TERMINALNO').agg(lambda arr: arr.iloc[0])
    #     print(t)

    return train, test
