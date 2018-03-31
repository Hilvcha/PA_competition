# coding : utf-8
import pandas as pd


def read_data(train_path, test_path):
    train = pd.read_csv(train_path, encoding='utf8')
    test = pd.read_csv(test_path, encoding='utf8')
    return train, test
