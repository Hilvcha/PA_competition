# coding : utf-8
from utils import data_utils
import pandas as pd


# 用户多次行程时间间隔的平均数
def wyj_trip_id_interval_mean(train, test):
    train_data = train.pivot_table(values=["TIME"],
                                   index=["TERMINALNO", "TRIP_ID"])
    td1 = train_data.groupby(['TERMINALNO'])
    tmp = []
    for i, value in td1:
        train_value = value["TIME"].values
        train_value.sort()
        train_mean = sum(train_value[1:] - train_value[:-1]) / (len(train_value) - 1) if len(train_value) > 1 else \
            train_value[0]
        tmp.append(train_mean)
    train_data = pd.DataFrame(tmp, index=[i + 1 for i in range(i)]).rename({0: "INTERVAL_MEAN"},
                                                                           axis='columns').rename_axis("TERMINALNO")
    # print(train_data)

    test_data = test.pivot_table(values=["TIME"],
                                 index=["TERMINALNO", "TRIP_ID"])
    td1 = test_data.groupby(['TERMINALNO'])
    tmp = []
    for i, value in td1:
        test_value = value["TIME"].values
        test_value.sort()
        test_mean = sum(test_value[1:] - test_value[:-1]) / (len(test_value) - 1) if len(test_value) > 1 else \
            test_value[0]
        tmp.append(test_mean)
    test_data = pd.DataFrame(tmp, index=[i + 1 for i in range(i)]).rename({0: "INTERVAL_MEAN"},
                                                                          axis='columns').rename_axis("TERMINALNO")

    data_utils.save_features(train_data, test_data, "trip_id_interval_mean")
