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
    train_df = pd.DataFrame(train_data)
    train_df.rename(columns={"TERMINALNO": "TRIP_ID_COUNT"}, inplace=True)

    test_data = test.groupby(["TERMINALNO"])["TERMINALNO"].count()
    test_df = pd.DataFrame(test_data)
    test_df.rename(columns={"TERMINALNO": "TRIP_ID_COUNT"}, inplace=True)

    return train_df, test_df
