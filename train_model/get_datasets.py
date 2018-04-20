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


def merge_datasets(train, test,slices):
    y_train = feature_utils.get_label(train)

    train_index = pd.Index(train['TERMINALNO'])
    test_index = pd.Index(test['TERMINALNO'])
    train_index = train_index.unique()
    test_index = test_index.unique()

    # 取出训练与测试集中的用户列
    train = pd.DataFrame(train_index, index=train_index)
    test = pd.DataFrame(test_index, index=test_index)

    # 加载记载在configure列表中的特征，并且合并
    for feature_name in Configure.features:
        #将不同块的特征concat起来
        print('pd merge', feature_name)
        train_feature, test_feature = data_utils.load_features(feature_name,slices)

        print(train_feature.columns,train_feature.shape,test_feature.shape)
        train = pd.merge(train, train_feature,
                         left_index=True,
                         right_index=True,how='left')
        test = pd.merge(test, test_feature,
                        left_index=True,
                        right_index=True,how='left')
    print(train.shape, test.shape, y_train.shape, test_index.shape)

    return train, test, y_train, test_index
