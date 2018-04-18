# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from utils.feature_utils import df_empty
# TERMINALNO,TIME,TRIP_ID,LONGITUDE,LATITUDE,DIRECTION,HEIGHT,SPEED,CALLSTATE,Y
# 对传入的表按trip_id分组，取每组的海拔的最大连续子数组，对每个人的所有行程的子数组取最大，平均, 方差。
def max_sub(arr):
    sum=0
    height=-999
    tempheight=arr.iloc[0]
    for h in arr:
        sum+=h-tempheight
        if sum>height:
            height=sum
        if sum<0:
            sum=0
        tempheight=h
    return sum

def height_feet(train,test):

    train_data=train[["TERMINALNO",'TRIP_ID','HEIGHT']].groupby(["TERMINALNO",'TRIP_ID'],as_index=False).agg(max_sub)

    max_train=train_data[["TERMINALNO",'HEIGHT']].groupby(["TERMINALNO"],as_index=True).max()
    mean_train=train_data[["TERMINALNO",'HEIGHT']].groupby(["TERMINALNO"],as_index=True).mean()
    var_train=train_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).var()
    train_data=pd.merge(max_train, mean_train, left_index=True, right_index=True)
    train_data=pd.merge(train_data, var_train, left_index=True, right_index=True)

    train_data.columns=['max_secc_inc','mean_secc_inc','var_secc_inc']

    test_data=test[["TERMINALNO",'TRIP_ID','HEIGHT']].groupby(["TERMINALNO",'TRIP_ID'],as_index=False).agg(max_sub)

    max_test=test_data[["TERMINALNO",'HEIGHT']].groupby(["TERMINALNO"],as_index=True).max()
    mean_test=test_data[["TERMINALNO",'HEIGHT']].groupby(["TERMINALNO"],as_index=True).mean()
    var_test=test_data[["TERMINALNO", 'HEIGHT']].groupby(["TERMINALNO"], as_index=True).var()
    test_data=pd.merge(max_test, mean_test, left_index=True, right_index=True)
    test_data=pd.merge(test_data, var_test, left_index=True, right_index=True)

    test_data.columns=['max_secc_inc','mean_secc_inc','var_secc_inc']
    return train_data,test_data
