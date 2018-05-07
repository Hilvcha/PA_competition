# -*- coding:utf-8 -*-

import time
import pandas as pd
from conf.configure import Configure
from functions.functions import save_all_features
from input.read_data import read_data
from train_model.xgboost_model import xgboost_train
from train_model.liner_model import liner_train
from train_model.lgb_model import lgb_train
# from train_model.catboost_model import cat_train
from train_model.ensemble import averaging_model

if __name__ == "__main__":
    now = time.localtime(time.time())
    print("******* start at:", time.strftime('%Y-%m-%d %H:%M:%S', now), '*******')
    # 程序入口
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)


    slices = 10
    train_slice_num = int(trainSet.TERMINALNO.max() / slices)
    test_slice_num = int(testSet.TERMINALNO.max() / slices)

    for s in range(slices):
        print("*****section", s, "******")
        train_start = train_slice_num * s
        train_end = train_slice_num * (s + 1)

        test_start = test_slice_num * s
        test_end = test_slice_num * (s + 1)
        if s == slices - 1:
            train_end += slices
            test_end += slices


        trainSection = trainSet[(trainSet['TERMINALNO'] >= train_start) & (trainSet['TERMINALNO'] < train_end)]
        testSection = testSet[(testSet['TERMINALNO'] >= test_start) & (testSet['TERMINALNO'] < test_end)]
        save_all_features(trainSection, testSection,s)

    # liner_train(trainSet,testSet,slices)
    lgb_train(trainSet, testSet,slices)
    # xgboost_train(trainSet, testSet,slices)
    # averaging_model(trainSet, testSet,slices)
    # cat_train(trainSet, testSet,slices)

