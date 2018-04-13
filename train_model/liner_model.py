# -*- coding:utf8 -*-
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from utils.feature_utils import time_this
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

from train_model.get_datasets import merge_datasets
from conf.configure import Configure


@time_this
def liner_train(train_set, test_set):
    train, test, train_label, test_index = merge_datasets(train_set, test_set)
    print(train.head(3))
    print('train.', train.axes)
    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)

    model = LinearRegression()
    model.fit(train, train_label)
    prediction = model.predict(test)
    pred_arr=[]
    for i in prediction:
        pred_arr.append(i[0])
    # 这里会否有更好的拼接方式？
    print(pred_arr,test_index)

    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


