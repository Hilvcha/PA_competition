# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd


def build_time_features(train, test):
    train_addtime=train
    test_addtime=test
    train_addtime['TIME_year'] = train_addtime['TIME'].dt.year
    train_addtime['TIME_month'] = train_addtime['TIME'].dt.month
    train_addtime['TIME_day'] = train_addtime['TIME'].dt.day
    train_addtime['TIME_weekofyear'] = train_addtime['TIME'].dt.weekofyear
    train_addtime['TIME_hour'] = train_addtime['TIME'].dt.hour
    train_addtime['TIME_minute'] = train_addtime['TIME'].dt.minute
    train_addtime['TIME_weekday'] = train_addtime['TIME'].dt.weekday
    train_addtime['TIME_is_weekend'] = train_addtime['TIME_weekday'].map(lambda d: 1 if (d == 0) | (d == 6)else 0)
    train_addtime['TIME_week_hour'] = train_addtime['TIME_weekday'] * 24 + train_addtime['TIME_hour']

    test_addtime['TIME_year'] = test_addtime['TIME'].dt.year
    test_addtime['TIME_month'] = test_addtime['TIME'].dt.month
    test_addtime['TIME_day'] = test_addtime['TIME'].dt.day
    test_addtime['TIME_weekofyear'] = test_addtime['TIME'].dt.weekofyear
    test_addtime['TIME_hour'] = test_addtime['TIME'].dt.hour
    test_addtime['TIME_minute'] = test_addtime['TIME'].dt.minute
    test_addtime['TIME_weekday'] = test_addtime['TIME'].dt.weekday
    test_addtime['TIME_is_weekend'] = test_addtime['TIME_weekday'].map(lambda d: 1 if (d == 0) | (d == 6)else 0)
    test_addtime['TIME_week_hour'] = test_addtime['TIME_weekday'] * 24 + test_addtime['TIME_hour']

    train_weekend=train_addtime[['TERMINALNO','TRIP_ID','TIME_is_weekend']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                               as_index=False).agg(lambda x: np.mean(pd.Series.mode(x)))
    train_weekend=train_weekend[['TERMINALNO','TIME_is_weekend']].groupby(['TERMINALNO'],
                                                               as_index=True).mean()
    test_weekend = test_addtime[['TERMINALNO', 'TRIP_ID', 'TIME_is_weekend']].groupby(['TERMINALNO', 'TRIP_ID'],
                                                                                        as_index=False).agg(
        lambda x: np.mean(pd.Series.mode(x)))
    test_weekend = test_weekend[['TERMINALNO', 'TIME_is_weekend']].groupby(['TERMINALNO'],
                                                                             as_index=True).mean()


    return train_weekend,test_weekend
