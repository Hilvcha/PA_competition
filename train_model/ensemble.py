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
import lightgbm as lgb
from utils.data_utils import merge_datasets
from conf.configure import Configure
from train_model.xgboost_model import xgboost_train
from train_model.lgb_model import lgb_train
from train_model.liner_model import liner_train


@time_this
def averaging_model(train_set, test_set, slices, n=0.7):
    train, test, train_label, test_index = merge_datasets(train_set, test_set, slices)
    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)
    # print('train.', train.axes)
    # print(train.dtypes)
    print(train_label.shape, train.shape)
    print(train.head(4))

    pred_lgb = lgb_train(train, train_label, test)
    pred_xgb = xgboost_train(train, train_label, test)
    pred_arr = pred_lgb

    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


if __name__ == '__main__':
    print('========== 加权融合 模型训练 ==========')
    # model_train()
