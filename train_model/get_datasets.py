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


def merge_datasets(train, test, slices):
    y_train = feature_utils.get_label(train)


    train_index = pd.Index(train['TERMINALNO'])
    test_index = pd.Index(test['TERMINALNO'])
    train_index = train_index.unique()
    test_index = test_index.unique()

    # 取出训练与测试集中的用户列
    train_data = pd.DataFrame(train_index, index=train_index)
    test_data = pd.DataFrame(test_index, index=test_index)

    # 加载记载在configure列表中的特征，并且合并
    for feature_name in Configure.features:
        # 将不同块的特征concat起来
        print('pd merge', feature_name)
        train_feature, test_feature = data_utils.load_features(feature_name, slices)

        print(train_feature.shape, test_feature.shape)
        train_data = pd.merge(train_data, train_feature,
                         left_index=True,
                         right_index=True, how='left')
        test_data = pd.merge(test_data, test_feature,
                        left_index=True,
                        right_index=True, how='left')
    print(train_data.shape, test_data.shape, y_train.shape, test_index.shape)


    return train_data, test_data, y_train, test_index
