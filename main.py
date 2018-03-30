# -*- coding:utf8 -*-
import os
import csv
import pandas as pd
from train_model.xgboost_model import model_train
from conf.configure import Configure
from features.speed_variance_mean import save_all_features

def init_path():
    Configure.base_path= os.path.abspath(os.path.join('.'))
    Configure.train_data = os.path.join(Configure.base_path, 'PINGAN-2018-train_demo.csv')
    Configure.test_data = os.path.join(Configure.base_path, 'PINGAN-2018-train_demo.csv')

    # train_data = '/data/dm/train.csv'
    # test_data =  '/data/dm/test.csv'
    # 数据清洗后的路径
    Configure.cleaned_path = os.path.join(Configure.base_path, 'cleaned')
    # 生成的特征的路径
    Configure.features_path = os.path.join(Configure.base_path, 'features')
    # 生成的模型可训练和预测的数据集
    Configure.datasets_path = os.path.join(Configure.base_path, 'datasets')
    # 最终结果csv存放处
    Configure.submit_result_path = os.path.abspath(os.path.join(Configure.base_path, 'model', 'submit.csv'))


if __name__ == "__main__":
    print("****************** start **********************")
    # 程序入口
    init_path()
    save_all_features()
    model_train()
