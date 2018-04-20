# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from utils.feature_utils import time_this
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import xgboost as xgb
from train_model.get_datasets import merge_datasets
from conf.configure import Configure


@time_this
def xgboost_train(train_set, test_set,slices):
    train, test, train_label, test_index = merge_datasets(train_set, test_set,slices)

    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)
    # print('train.', train.axes)
    # print(train.dtypes)
    print(train_label.shape, train.shape)
    x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)

    d_train = xgb.DMatrix(x_train, label=y_train)
    # print(d_train)
    d_val = xgb.DMatrix(x_val, label=y_val)
    param = {
        'learning_rate': 0.1,
        'n_estimators': 1000,
        'max_depth': 3,
        'min_child_weight': 5,
        'gamma': 0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'eta': 0.05,
        'silent': 1,
        'objective': 'reg:linear',
        'eval_metric': 'rmse'
    }

    num_round = 100
    eval_list = [(d_val, 'eval'), (d_train, 'train')]
    bst = xgb.train(param, d_train, num_round, eval_list, early_stopping_rounds=100)
    d_test = xgb.DMatrix(test)
    prediction = bst.predict(d_test)
    # 这里会否有更好的拼接方式？
    pred_arr = np.array(prediction)
    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


if __name__ == '__main__':
    print('========== xgboost 模型训练 ==========')
    # model_train()
# 日志详情
# ******* start at: 2018-04-20 01:08:28 ******* \
#     input.read_data.read_data:5148.18
# seconds *****section 0 ******
# functions.functions.save_all_features:5348.98 seconds
# *****section 1 ******
# functions.functions.save_all_features:4981.69 seconds
# pd merge build_time_features
# (33454, 11) (14045, 11) (33455, 1) (14046,)
#  maxTime phonerisk dir_risk height_risk speed_max TERMINALNO
# 1 4920.0 43.46149
# 2 2061.953853 311.159931 30.934708 2 1860.0 48.487930 399.247677 397.850743 20.540089 3 2760.0 43.118034 470.008747 267.205415 32.200820
# speed_mean height_mean Zao Wan Sheye TERMINALNO
#  1 18.033800 6.563380 1.0 0.0 1.0 2 9.113635 13.634106 1.0 0.0 1.0 3 19.513882 10.519737 1.0 0.0 1.0
# Traceback (most recent call last):
# File "/data/share/jingsuan/js_project/1825122096_1825122096/_PA_competition/main.py", line 39, in <module> xgboost_train(trainSet, testSet,slices)
# File "/data/share/jingsuan/js_project/1825122096_1825122096/_PA_competition/utils/feature_utils.py", line 10, in wrapper r = func(*args, **kwargs)
# File "/data/share/jingsuan/js_project/1825122096_1825122096/_PA_competition/train_model/xgboost_model.py",
# line 27, in xgboost_train x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)
# File "/usr/local/python3/lib/python3.6/site-packages/sklearn/model_selection/_split.py", line 2031, in train_test_split arrays = indexable(*arrays)
# File "/usr/local/python3/lib/python3.6/site-packages/sklearn/utils/validation.py", line 229, in indexable check_consistent_length(*result)
# File "/usr/local/python3/lib/python3.6/site-packages/sklearn/utils/validation.py", line 204, in check_consistent_length "samples: %r" % [int(l) for l in lengths])
# ValueError: Found input variables with inconsistent numbers of samples: [33454, 33455]
