# coding: utf-8
# made by rxd
import pandas as pd


def callstate_feat(train, test):
    train_data = train[['TERMINALNO', 'TRIP_ID', 'CALLSTATE']]
    test_data = test[['TERMINALNO', 'TRIP_ID', 'CALLSTATE']]

    call_data_train = pd.get_dummies(train['CALLSTATE'], prefix='call_state_')
    call_data_test = pd.get_dummies(test['CALLSTATE'], prefix='call_state_')
    train_data = pd.concat([train_data, call_data_train], axis=1)
    test_data = pd.concat([test_data, call_data_test], axis=1)

    train_data = train_data.groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).sum()
    del train_data['TRIP_ID']
    train_data = train_data.groupby('TERMINALNO').mean()
    test_data = test_data.groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).sum()
    del test_data['TRIP_ID']
    test_data = test_data.groupby('TERMINALNO').mean()
    return train_data, test_data
