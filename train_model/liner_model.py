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

from utils.data_utils import merge_datasets
from conf.configure import Configure


@time_this
def liner_train(train, train_label,test):

    # print(train.iloc[:,[0,1,2]].head(1),test.iloc[:,[0,1,2]].head(1))
    # print('train.', train.axes)
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

    # 这里会否有更好的拼接方式？

    return prediction
