# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from os import listdir
from os.path import isfile, join
import pickle
import numpy as np
import pandas as pd
from conf.configure import Configure


def load_features(feature_name):
    train_path = os.path.join(Configure.features_path, 'train_' + feature_name + '.pkl')
    test_path = os.path.join(Configure.features_path, 'test_' + feature_name + '.pkl')

    with open(train_path, 'rb') as f:
        train = pickle.load(f)
    with open(test_path, 'rb') as f:
        test = pickle.load(f)

    return train, test


def save_features(train, test, feature_name):
    if train is not None:
        train_path = os.path.join(Configure.features_path, 'train_' + feature_name + '.pkl')
        with open(train_path, 'wb') as f:
            pickle.dump(train, f, -1)
    if test is not None:
        train_path = os.path.join(Configure.features_path, 'test_' + feature_name + '.pkl')
        with open(train_path, 'wb') as f:
            pickle.dump(train, f, -1)
