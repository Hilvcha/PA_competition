# coding: utf-8
import os
import sys

# wyj
module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

# remove warnings
# import warnings
# warnings.filterwarnings('ignore')

from conf.configure import Configure
from .read_data import read_data

# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

from functions.trip_id_count import wyj_trip_id_count
from functions.trip_id_interval_mean import wyj_trip_id_interval_mean
from .speed_variance_mean import wyj_speed_variance_mean


def save_all_features():
    funcs = {
        'speed_variance_mean': wyj_speed_variance_mean,
        # 每名用户的行程数
        'trip_id_count': wyj_trip_id_count,
        # 用户多次行程时间间隔的平均数
        'trip_id_interval_mean': wyj_trip_id_interval_mean,
    }
    train, test = read_data(Configure.train_data, Configure.test_data)
    for name in Configure.features:
        funcs[name](train, test)


if __name__ == "__main__":
    print("****************** feature **********************")

    # 程序入口
    save_all_features()
