# coding : utf-8
from utils import data_utils
import numpy as np


def wyj_speed_variance_mean(train, test):
    train_data = train.pivot_table(values=["SPEED"],
                                   index=["TERMINALNO", "TRIP_ID"],
                                   aggfunc=[np.var])
    train_data.fillna(0, inplace=True)
    train_data = train_data.groupby(["TERMINALNO"]).mean()
    # print(train_data)

    test_data = test.pivot_table(values=["SPEED"],
                                 index=["TERMINALNO", "TRIP_ID"],
                                 aggfunc=[np.var])
    test_data.fillna(0, inplace=True)
    test_data = test_data.groupby(["TERMINALNO"]).mean()
    # print(train_data.shape)
    data_utils.save_features(train_data, test_data, "speed_variance_mean")
