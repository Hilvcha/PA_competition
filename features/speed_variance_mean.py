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
    train_data = train.pivot_table(values=['SPEED'],
                                   index=["TERMINALNO", "TRIP_ID"],
                                   aggfunc=[np.var], )
    train_data.fillna(0, inplace=True)
    train_data = train_data.groupby(['TERMINALNO']).mean()

    test_data = test.pivot_table(values=['SPEED'],
                                 index=["TERMINALNO", "TRIP_ID"],
                                 aggfunc=[np.var], )
    test_data.fillna(0, inplace=True)
    test_data = test_data.groupby(['TERMINALNO']).mean()
    data_utils.save_features(train_data, test_data, 'speed_variance_mean')

# # 每名用户的行程数
#         'trip_id_count' : {'on': 'TERMINALNO', 'how': 'left'},
#         #用户多次行程时间间隔的平均数
#         'trip_id_interval_mean' : {'on': 'TERMINALNO', 'how': 'left'},
# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

def wyj_trip_id_count():
    pass

def  wyj_trip_id_interval_mean():
    pass

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
