# -*- coding:utf-8 -*-

import time

from conf.configure import Configure
from functions.functions import save_all_features
from input.read_data import read_data
from train_model.xgboost_model import xgboost_train
from train_model.liner_model import liner_train

if __name__ == "__main__":
    now=time.localtime(time.time())
    print("******* start at:", time.strftime('%Y-%m-%d %H:%M:%S',now ), '*******')
    # 程序入口
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)

    save_all_features(trainSet, testSet)

    # liner_train(trainSet,testSet)

    xgboost_train(trainSet, testSet)

    print("******* start at:", time.strftime('%Y-%m-%d %H:%M:%S',now ), '*******')

