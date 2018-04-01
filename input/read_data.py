# coding : utf-8
import pandas as pd


def read_data(train_path, test_path):
    dtypes_train = {
        'TERMINALNO': 'uint32',
        'TIME': 'uint16',
        'TRIP_ID': 'uint8',
        'LATITUDE': 'float32',
        'LONGITUDE': 'float32',
        'DIRECTION': 'uint8',
        'HEIGHT': 'float32',
        'SPEED': 'float32',
        'CALLSTATE': 'uint8',
        'Y': 'float32'
    }
    dtypes_test = {
        'TERMINALNO': 'uint32',
        'TIME': 'uint16',
        'TRIP_ID': 'uint8',
        'LATITUDE': 'float32',
        'LONGITUDE': 'float32',
        'DIRECTION': 'uint8',
        'HEIGHT': 'float32',
        'SPEED': 'float32',
        'CALLSTATE': 'uint8',
    }
    train = pd.read_csv(train_path, encoding='utf8', dtype=dtypes_train)
    test = pd.read_csv(test_path, encoding='utf8', dtype=dtypes_test)
    return train, test
