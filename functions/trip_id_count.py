# coding : utf-8
# created by cjr
import pandas as pd


def trip_id_count(train, test):
    """
    每名用户的行程数
    :param train:
    :param test:
    :return:
    """
    train_data = train.groupby(["TERMINALNO"])["TRIP_ID"].max()
    train_df = pd.DataFrame(train_data)
    train_df.rename(columns={"TRIP_ID": "TRIP_ID_COUNT"}, inplace=True)

    test_data = test.groupby(["TERMINALNO"])["TRIP_ID"].max()
    test_df = pd.DataFrame(test_data)
    test_df.rename(columns={"TRIP_ID": "TRIP_ID_COUNT"}, inplace=True)
    return train_df, test_df
