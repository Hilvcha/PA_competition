# coding: utf-8
import os
import sys

# wyj
module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

# remove warnings
import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from conf.configure import Configure
from utils import data_utils, feature_utils

# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

train = pd.read_csv(Configure.train_data, encoding='utf8')
test = pd.read_csv(Configure.test_data, encoding='utf8')


def wyj_speed_variance_mean():
    train_data = train.pivot_table(values=["SPEED"],
                                   index=["TERMINALNO", "TRIP_ID"],
                                   aggfunc=[np.var])
    train_data.fillna(0, inplace=True)
    train_data = train_data.groupby(["TERMINALNO"]).mean()
    print(train_data)

    test_data = test.pivot_table(values=["SPEED"],
                                 index=["TERMINALNO", "TRIP_ID"],
                                 aggfunc=[np.var])
    test_data.fillna(0, inplace=True)
    test_data = test_data.groupby(["TERMINALNO"]).mean()
    data_utils.save_features(train_data, test_data, "speed_variance_mean")


# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y


# 每名用户的行程数
def wyj_trip_id_count():
    train_data = train.groupby(["TERMINALNO"])["TERMINALNO"].count()
    train_df = pd.DataFrame(train_data).rename({0: "TRIP_ID_COUNT"}, axis='columns')

    test_data = test.groupby(["TERMINALNO"])["TERMINALNO"].count()
    test_df = pd.DataFrame(test_data).rename({0: "TRIP_ID_COUNT"}, axis='columns')

    data_utils.save_features(train_df, test_df, "trip_id_count")


# 用户多次行程时间间隔的平均数
def wyj_trip_id_interval_mean():
    train_data = train.pivot_table(values=["TIME"],
                                   index=["TERMINALNO", "TRIP_ID"])
    td1 = train_data.groupby(['TERMINALNO'])
    tmp = []
    for i, value in td1:
        train_value = value["TIME"].values
        train_value.sort()
        train_mean = sum(train_value[1:] - train_value[:-1]) / (len(train_value) - 1) if len(train_value) > 1 else \
        train_value[0]
        tmp.append([i + 1, train_mean])
    train_data = pd.DataFrame(tmp).rename({0: "TERMINALNO", 1: "INTERVAL_MEAN"}, axis='columns')

    test_data = test.pivot_table(values=["TIME"],
                                 index=["TERMINALNO", "TRIP_ID"])
    td1 = test_data.groupby(['TERMINALNO'])
    tmp = []
    for i, value in td1:
        test_value = value["TIME"].values
        test_value.sort()
        test_mean = sum(test_value[1:] - test_value[:-1]) / (len(test_value) - 1) if len(test_value) > 1 else \
        test_value[0]
        tmp.append([i + 1, test_mean])
    test_data = pd.DataFrame(tmp, columns=["TERMINALNO", "INTERVAL_MEAN"])
    data_utils.save_features(train_data, test_data, "trip_id_interval_mean")


def save_all_features():
    if 'speed_variance_mean' in Configure.features:
        wyj_speed_variance_mean()
    if 'trip_id_count' in Configure.features:
        wyj_trip_id_count()
    if 'trip_id_interval_mean' in Configure.features:
        wyj_trip_id_interval_mean()


if __name__ == "__main__":
    print("****************** feature **********************")

    # 程序入口
    save_all_features()
