# -*- coding:utf-8 -*-

import time
import pandas as pd
from conf.configure import Configure
from functions.functions import save_all_features
from input.read_data import read_data
from train_model.xgboost_model import xgboost_train
from train_model.liner_model import liner_train

if __name__ == "__main__":
    now=time.localtime(time.time())
    print("******* start at:", time.strftime('%Y-%m-%d %H:%M:%S',now ), '*******')
    # 程序入口
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path,4)

    slices = 4
    for s in range(slices):
        print("*****section", s, "******")
        slice_num = int(trainSet.TERMINALNO.max() / slices)
        start = slice_num * s
        end = slice_num(s + 1)
        if s == slices - 1:
            end += slices
        trainSet = trainSet[(trainSet['TERMINALNO'] > start) & (trainSet['TERMINALNO'] <= end)]
        save_all_features(trainSet, testSet,s)

    # liner_train(trainSet,testSet)

        xgboost_train(trainSet, testSet,slices)


