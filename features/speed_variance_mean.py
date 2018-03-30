import os
import sys
#wyj
module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)
base_path = os.path.abspath(os.path.join('..'))
# remove warnings
import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from conf.configure import Configure
from utils import data_utils,feature_utils
#TERMINALNO,TIME,TRIP_ID,LONGITUDE,LATITUDE,DIRECTION,HEIGHT,SPEED,CALLSTATE,Y

train = pd.read_csv(Configure.train_data, encoding='utf8')
test = pd.read_csv(Configure.train_data, encoding='utf8')


def wyj_speed_variance_mean():

    #按用户分出他的所有行程

    train_data = train.pivot_table(values=['SPEED'],
                           index=["TERMINALNO", "TRIP_ID"],
                           aggfunc=[ np.var],)
    train_data.fillna(0,inplace=True)
    train_data=train_data.groupby(['TERMINALNO']).mean()

    test_data = test.pivot_table(values=['SPEED'],
                              index=["TERMINALNO", "TRIP_ID"],
                              aggfunc=[np.var], )
    test_data.fillna(0, inplace=True)
    test_data = test_data.groupby(['TERMINALNO']).mean()
    # values：需要对哪些字段应用函数
    # index：透视表的行索引(row)
    # columns：透视表的列索引(column)
    # aggfunc：应用什么函数
    # fill_value：空值填充
    # margins：添加汇总项

    # train=train[['TERMINALNO','TRIP_ID','SPEED']].groupby(['TERMINALNO','TRIP_ID']).size()
    # print(train)
    # train=train[['TERMINALNO','SPEED']].agg(np.mean)
    data_utils.save_features(train_data,test_data,'speed_variance_mean')


def save_all_features():

    if 'speed_variance_mean' in Configure.features:
        wyj_speed_variance_mean()

if __name__ == "__main__":
    print("****************** feature **********************")
    # 程序入口
    save_all_features()

