import pandas as pd
import numpy as np
import time
import os
import csv

path_train_input = "/data/dm/train.csv"  # 训练文件
path_test_input = "/data/dm/test.csv"  # 测试文件
path_test_out = "model/"
# the real train_data read nrows=17940000
train_data = pd.read_csv(path_train_input, usecols=['TERMINALNO', 'TIME', 'TRIP_ID', 'CALLSTATE', 'DIRECTION', 'Y'])
test_data = pd.read_csv(path_test_input, usecols=['TERMINALNO', 'TIME', 'TRIP_ID', 'CALLSTATE', 'DIRECTION'])


# train_data = pd.read_csv('PINGAN-2018-train_demo.csv',
#                          usecols=['TERMINALNO', 'TIME', 'TRIP_ID', 'CALLSTATE', 'DIRECTION', 'Y'], nrows=35000)
# test_data = pd.read_csv('PINGAN-2018-train_demo.csv',
#                         usecols=['TERMINALNO', 'TIME', 'TRIP_ID', 'CALLSTATE', 'DIRECTION'], nrows=20000)


def fun(arr):
    return arr.iloc[0]


def get_label(df):
    df = df[['TERMINALNO', 'Y']].groupby('TERMINALNO', as_index=False).agg(fun)
    return df['Y']


train_label = get_label(train_data)


# 时间戳转化
def time_help(x):
    timeArray = time.localtime(x)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeArray)


# 将数据集中的时间戳转化为时间
train_data.TIME = pd.to_datetime(train_data.TIME.apply(lambda x: time_help(x)), format='%Y-%m-%d %H:%M:%S')
test_data.TIME = pd.to_datetime(test_data.TIME.apply(lambda x: time_help(x)), format='%Y-%m-%d %H:%M:%S')


# 对数据按照时间顺序排序
def sort_by_time(train, test):
    train = train.sort_values(by='TIME')
    test = test.sort_values(by='TIME')
    return train, test


train_data, test_data = sort_by_time(train_data, test_data)


# 行程方向变化方差
def fun_direction(arr):
    ss = []
    m = (len(arr) - 1)
    try:
        if (m == 0):
            return 0
        mean_d = (abs(arr.iloc[-1] - arr.iloc[0]) % 360) / m
        for i in range(len(arr) - 1):
            ss.append(abs(abs(arr.iloc[i + 1] - arr.iloc[i]) % 360 - mean_d))
        return sum(ss) / m
    except:
        return 0


# 统计历史中方向无法获取次数
def fun_direction_none(arr):
    ll = 0
    for i in range(len(arr)):
        if arr.iloc[i] == -1:
            ll += 1
    return ll


def direction_change_feat(train, test):
    train_1 = train[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction_none)
    test_1 = test[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction_none)
    train_1 = train_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO', as_index=False).mean()
    test_1 = test_1[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO', as_index=False).mean()
    train_1.rename(columns={'DIRECTION': 'direction_none'}, inplace=True)
    test_1.rename(columns={'DIRECTION': 'direction_none'}, inplace=True)
    # 删除包含有方向为-1的行
    ex_list = list(train.DIRECTION)
    ex_list.remove(-1)
    train = train[train.DIRECTION.isin(ex_list)]
    test = test[test.DIRECTION.isin(ex_list)]

    train = train[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction)
    test = test[['TERMINALNO', 'TRIP_ID', 'DIRECTION']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).agg(
        fun_direction)
    train = train[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO', as_index=False).mean()
    test = test[['TERMINALNO', 'DIRECTION']].groupby('TERMINALNO', as_index=False).mean()
    train = pd.merge(train, train_1, on='TERMINALNO', how='left')
    test = pd.merge(test, test_1, on='TERMINALNO', how='left')
    return train, test


train_data_direction_feat, test_data_direction_feat = direction_change_feat(train_data, test_data)


def callstate_feat(train, test):
    call_data_train = pd.get_dummies(train['CALLSTATE'], prefix='call_state_')
    call_data_test = pd.get_dummies(test['CALLSTATE'], prefix='call_state_')
    train = pd.concat([train, call_data_train], axis=1)
    test = pd.concat([test, call_data_test], axis=1)
    del train['Y']
    del train['DIRECTION']
    del train['TIME']
    del train['CALLSTATE']
    del test['DIRECTION']
    del test['TIME']
    del test['CALLSTATE']
    train = train.groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).sum()
    del train['TRIP_ID']
    train = train.groupby('TERMINALNO', as_index=False).mean()
    test = test.groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).sum()
    del test['TRIP_ID']
    test = test.groupby('TERMINALNO', as_index=False).mean()
    return train, test


train_data_feat_call, test_data_feat_call = callstate_feat(train_data, test_data)

train_data = pd.merge(train_data_direction_feat, train_data_feat_call, on='TERMINALNO', how='left')
test_data = pd.merge(test_data_direction_feat, test_data_feat_call, on='TERMINALNO', how='left')

Id = test_data['TERMINALNO']
Id = list(Id)
del train_data['TERMINALNO']
del test_data['TERMINALNO']
from sklearn.model_selection import train_test_split

x_train, x_val, y_train, y_val = train_test_split(train_data, train_label, test_size=0.2, random_state=100)
import xgboost as xgb

print('start running ....')
dtrain = xgb.DMatrix(x_train, label=y_train)
dval = xgb.DMatrix(x_val, label=y_val)
param = {'learning_rate': 0.1,
         'n_estimators': 1000,
         'max_depth': 3,
         'min_child_weight': 5,
         'gamma': 0,
         'subsample': 0.8,
         'colsample_bytree': 0.8,
         'eta': 0.05,
         'silent': 1,
         'objective': 'reg:linear'
         }

num_round = 50
plst = list(param.items())
plst += [('eval_metric', 'auc')]
evallist = [(dval, 'eval'), (dtrain, 'train')]
bst = xgb.train(plst, dtrain, num_round, evallist, early_stopping_rounds=100)
dtest = xgb.DMatrix(test_data)
Pred = bst.predict(dtest)
Pred = list(Pred)


def process(Id, Pred):
    with(open(os.path.join(path_test_out, "test.csv"), mode="w")) as outer:
        writer = csv.writer(outer)
        i = 0
        for l in range(len(Id) + 1):
            if (i == 0):
                i += 1
                writer.writerow(["Id", "Pred"])
                continue
            writer.writerow([Id[l - 1], Pred[l - 1]])


process(Id, Pred)
