# coding: utf-8
import os
import sys
import pandas as pd

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

import pickle
from conf.configure import Configure
from utils.feature_utils import get_label

def load_features(feature_name, slices):
    train_path = os.path.join(Configure.features_path, 'train_' + feature_name + '_' + '0' + '.pkl')
    test_path = os.path.join(Configure.features_path, 'test_' + feature_name + '_' + '0' + '.pkl')

    with open(train_path, 'rb') as f:
        train = pickle.load(f)
    with open(test_path, 'rb') as f:
        test = pickle.load(f)
    for i in range(slices):
        if i == 0:
            continue
        train_path = os.path.join(Configure.features_path, 'train_' + feature_name + '_' + str(i) + '.pkl')
        test_path = os.path.join(Configure.features_path, 'test_' + feature_name + '_' + str(i) + '.pkl')
        with open(train_path, 'rb') as f:
            temptrain = pickle.load(f)
        with open(test_path, 'rb') as f:
            temptest = pickle.load(f)
        train = pd.concat([train, temptrain])
        test = pd.concat([test, temptest])

    return train, test


def save_features(data, datatype, feature_name, s):
    if data is not None:
        data_path = os.path.join(Configure.features_path, datatype + '_' + feature_name + '_' + str(s) + '.pkl')
        with open(data_path, 'wb') as f:
            pickle.dump(data, f, -1)


def merge_datasets(train, test, slices):
    y_train = get_label(train)


    train_index = pd.Index(train['TERMINALNO'])
    test_index = pd.Index(test['TERMINALNO'])
    train_index = train_index.unique()
    test_index = test_index.unique()

    # 取出训练与测试集中的用户列
    train = pd.DataFrame(train_index, index=train_index)
    test = pd.DataFrame(test_index, index=test_index)

    # 加载记载在configure列表中的特征，并且合并
    for feature_name in Configure.features:
        # 将不同块的特征concat起来
        print('pd merge', feature_name)
        train_feature, test_feature = load_features(feature_name, slices)

        print(train_feature.shape, test_feature.shape)
        train = pd.merge(train, train_feature,
                         left_index=True,
                         right_index=True, how='left')
        test = pd.merge(test, test_feature,
                        left_index=True,
                        right_index=True, how='left')
    print(train.shape, test.shape, y_train.shape, test_index.shape)


    return train, test, y_train, test_index
