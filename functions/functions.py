# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from conf.configure import Configure
from utils import data_utils

# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

from functions.trip_id_count import wyj_trip_id_count
from functions.trip_id_interval_mean import wyj_trip_id_interval_mean
from functions.speed_variance_mean import wyj_speed_variance_mean
from functions.speed_first_mean import wyj_speed_first_mean


def save_all_features(train, test):
    funcs = {
        'speed_variance_mean': wyj_speed_variance_mean,
        'trip_id_count': wyj_trip_id_count,
        'trip_id_interval_mean': wyj_trip_id_interval_mean,
        'speed_first_mean': wyj_speed_first_mean
    }
    for name in Configure.features:
        data_utils.save_features(*funcs[name](train, test), name)


if __name__ == "__main__":
    print("****************** feature **********************")
    # 程序入口
    # save_all_features()
