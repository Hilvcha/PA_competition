# -*- coding:utf-8 -*-

from train_model.xgboost_model import model_train
from functions.functions import save_all_features


if __name__ == "__main__":
    print("****************** start **********************")
    # 程序入口
    save_all_features()
    model_train()
