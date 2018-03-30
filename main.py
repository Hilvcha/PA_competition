# -*- coding:utf8 -*-
import os
import csv
import pandas as pd
from train_model.xgboost_model import model_train
from conf.configure import Configure
from features.speed_variance_mean import save_all_features




if __name__ == "__main__":
    print("****************** start **********************")
    # 程序入口

    save_all_features()
    model_train()
