# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)
import time

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import auc, roc_curve
from train_model.get_datasets import load_datasets
from conf.configure import Configure
from utils import feature_utils


def abs_convert(rand):
    return abs(rand)


def model_train():
    train, test, train_label, index_test = load_datasets()
    print(train, test, train_label)
    test.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    Id = test['Id']
    del train['TERMINALNO']
    del test['Id']
    x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.2, random_state=100)

    dtrain = xgb.DMatrix(x_train, label=y_train)
    dval = xgb.DMatrix(x_val, label=y_val)
    param = {'learning_rate': 0.1,
             'n_estimators': 1000,
             'max_depth': 2,
             'min_child_weight': 7,
             'gamma': 0,
             'subsample': 0.8,
             'colsample_bytree': 0.8,
             'eta': 0.05,
             'silent': 1,
             'objective': 'reg:linear'
             }

    num_round = 70
    plst = list(param.items())
    plst += [('eval_metric', 'auc')]
    evallist = [(dval, 'eval'), (dtrain, 'train')]
    bst = xgb.train(plst, dtrain, num_round, evallist, early_stopping_rounds=100)
    dtest = xgb.DMatrix(test)
    Pred = bst.predict(dtest)
    Pred = np.array(Pred)

    Pred = pd.Series(Pred, name='Pred', index=index_test)
    print(Id, Pred)

    print(Id.describe(), Pred.describe())
    submit_df = pd.concat([Id, Pred], axis=1)
    print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


if __name__ == '__main__':
    print('========== xgboost 模型训练 ==========')

    model_train()
