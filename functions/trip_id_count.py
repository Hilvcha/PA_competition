# coding : utf-8
from utils import data_utils
import pandas as pd


# 每名用户的行程数
def wyj_trip_id_count(train, test):
    train_data = train.groupby(["TERMINALNO"])["TERMINALNO"].count()
    train_df = pd.DataFrame(train_data).rename({"TERMINALNO": "TRIP_ID_COUNT"}, axis='columns')

    test_data = test.groupby(["TERMINALNO"])["TERMINALNO"].count()
    test_df = pd.DataFrame(test_data).rename({"TERMINALNO": "TRIP_ID_COUNT"}, axis='columns')

    # print(train_df)

    data_utils.save_features(train_df, test_df, "trip_id_count")
