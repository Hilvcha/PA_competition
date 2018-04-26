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
from train_model.get_datasets import merge_datasets
from conf.configure import Configure


@time_this
def lgb_train(train_set, test_set, slices):
    train, test, train_label, test_index = merge_datasets(train_set, test_set, slices)
    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)
    # print('train.', train.axes)
    # print(train.dtypes)
    print(train_label.shape, train.shape)
    print(train.head(4))
    train_label=train_label['Y']
    x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)

    train_data = lgb.Dataset(x_train, label=y_train.ravel())
    test_data1 = lgb.Dataset(x_val, label=y_val.ravel())


    param = {'num_leaves': 31,
             'num_trees': 33,
             'metric': 'rmse',
             'is_unbalance': 'true',
            }

    num_round = 10
    bst = lgb.train(param, train_data, num_round, valid_sets=test_data1)
    prediction = bst.predict(test)
    # Pred = list(Pred)
    # d_train = xgb.DMatrix(x_train, label=y_train)
    # # print(d_train)
    # d_val = xgb.DMatrix(x_val, label=y_val)
    # param = {
    #     'learning_rate': 0.1,
    #     'n_estimators': 1000,
    #     'max_depth': 3,
    #     'min_child_weight': 5,
    #     'gamma': 0,
    #     'subsample': 0.8,
    #     'colsample_bytree': 0.8,
    #     'eta': 0.05,
    #     'silent': 1,
    #     'objective': 'reg:linear',
    #     'eval_metric': 'rmse'
    # }
    #
    # num_round = 100
    # eval_list = [(d_val, 'eval'), (d_train, 'train')]
    # bst = xgb.train(param, d_train, num_round, eval_list, early_stopping_rounds=100)
    # d_test = xgb.DMatrix(test)
    # prediction = bst.predict(d_test)
    # 这里会否有更好的拼接方式？
    pred_arr = np.array(prediction)
    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)



if __name__ == '__main__':
    print('========== lgb 模型训练 ==========')
    # model_train()
