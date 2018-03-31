# coding : utf-8
import pandas as pd


def wyj_trip_id_count(train, test):
    """
    每名用户的行程数
    :param train:
    :param test:
    :return:
    """
    train_data = train.groupby(["TERMINALNO"])["TERMINALNO"].count()
    train_df = pd.DataFrame(train_data).rename({"TERMINALNO": "TRIP_ID_COUNT"}, axis='columns')

    test_data = test.groupby(["TERMINALNO"])["TERMINALNO"].count()
    test_df = pd.DataFrame(test_data).rename({"TERMINALNO": "TRIP_ID_COUNT"}, axis='columns')

    # print(train_df)
    return train_df, test_df
