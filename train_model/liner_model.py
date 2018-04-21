# -*- coding:utf8 -*-
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from utils.feature_utils import time_this
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression,HuberRegressor,Ridge,Lasso,PassiveAggressiveRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

import pandas as pd

from train_model.get_datasets import merge_datasets
from conf.configure import Configure


@time_this
def liner_train(train_set, test_set,slices):
    train, test, train_label, test_index = merge_datasets(train_set, test_set,slices)
    # print(train.iloc[:,[0,1,2]].head(1),test.iloc[:,[0,1,2]].head(1))
    # print('train.', train.axes)
    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)

    # 岭回归
    linreg = Ridge(normalize=True, max_iter=2000, solver="sparse_cg")
    linreg.fit(train, train_label)
    prediction = linreg.predict(test)
    # *********************************************************

    # 线性回归
    # model = LinearRegression()
    # model.fit(train, train_label)
    # prediction = model.predict(test)
    # print(prediction)

    pred_arr=[]
    for i in prediction:
        pred_arr.append(i[0])
    # 这里会否有更好的拼接方式？

    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


