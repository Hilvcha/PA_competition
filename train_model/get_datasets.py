# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

# remove warnings
import warnings

warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
from conf.configure import Configure
from utils import feature_utils, data_utils


def load_datasets():
    # 原始数据集
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

    train = pd.read_csv(Configure.train_data, encoding='utf8', dtype=dtypes_train)
    test = pd.read_csv(Configure.test_data, encoding='utf8', dtype=dtypes_test)


def load_datasets():
    # 原始数据集
    train = pd.read_csv(Configure.train_data, encoding='utf8')
    test = pd.read_csv(Configure.test_data, encoding='utf8')

    y_train = feature_utils.get_label(train)

    index_train = pd.Index(train['TERMINALNO'])
    index_test = pd.Index(test['TERMINALNO'])
    index_train = index_train.unique()
    index_test = index_test.unique()

    # 取出训练与测试集中的用户列
    train = pd.DataFrame(index_train, index=index_train)
    test = pd.DataFrame(index_test, index=index_test)

    # 加载记载在configure列表中的特征，并且合并
    features_merged_dict = Configure.features
    for feature_name in Configure.features:
        print('pd merge', feature_name)
        train_feature, test_feature = data_utils.load_features(feature_name)
        train = pd.merge(train, train_feature,
                         left_index=True,
                         right_index=True)
        test = pd.merge(test, test_feature,
                        left_index=True,
                        right_index=True)
    return train, test, y_train, index_test