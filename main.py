# -*- coding:utf-8 -*-

from train_model.xgboost_model import model_train
from conf.configure import Configure
from functions.functions import save_all_features
from input.read_data import read_data


if __name__ == "__main__":
    print("****************** start **********************")
    # 程序入口
    trainSet, testSet = read_data(Configure.train_path, Configure.test_path)

    save_all_features(trainSet, testSet)
    
    # model_train(trainSet, testSet)
