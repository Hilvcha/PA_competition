
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
from utils import feature_utils,data_utils

def load_datasets():
    #原始数据集
    train = pd.read_csv(Configure.train_data,encoding='utf8')
    test = pd.read_csv(Configure.test_data,encoding='utf8')
    y_train=feature_utils.get_label(train)
    y_test=feature_utils.get_label(test)
    #取出训练与测试集中的用户列
    test,train=test['TERMINALNO'],train['TERMINALNO']
    test,train=test.drop_duplicates(),train.drop_duplicates()
    #加载记载在configure列表中的特征，并且合并
    features_merged_dict = Configure.features
    for feature_name in Configure.features:
        print('pd merge',feature_name)
        train_feature, test_feature = data_utils.load_features(feature_name)
        train = pd.merge(train, train_feature,
                         on=features_merged_dict[feature_name]['on'],
                         how=features_merged_dict[feature_name]['how'])
        test = pd.merge(test, test_feature,
                        on=features_merged_dict[feature_name]['on'],
                        how=features_merged_dict[feature_name]['how'])
    return train,test,y_train,y_test













