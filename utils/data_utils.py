# coding: utf-8
import os
import sys
import pandas as pd

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

import pickle
from conf.configure import Configure


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

