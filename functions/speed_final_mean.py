# coding : utf-8
# created by wyj
import pandas as pd


# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

def speed_final_mean(train, test):
    train_data = train[['TERMINALNO', 'TRIP_ID', 'SPEED']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).mean()
    train_final_data = train_data[['TERMINALNO', 'SPEED']].groupby(['TERMINALNO']).agg(lambda arr: arr.iloc[-1])
    train_mean_data = train_data[['TERMINALNO', 'SPEED']].groupby(['TERMINALNO']).mean()

    test_data = test[['TERMINALNO', 'TRIP_ID', 'SPEED']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).mean()
    test_final_data = test_data[['TERMINALNO', 'SPEED']].groupby(['TERMINALNO']).agg(lambda arr: arr.iloc[-1])
    test_mean_data = test_data[['TERMINALNO', 'SPEED']].groupby(['TERMINALNO']).mean()

    train_final_data.rename(columns={'SPEED': 'SPEED_FINAL_MEAN'}, inplace=True)
    test_final_data.rename(columns={'SPEED': 'SPEED_FINAL_MEAN'}, inplace=True)

    train_mean_data.rename(columns={'SPEED': 'SPEED_MEAN'}, inplace=True)
    test_mean_data.rename(columns={'SPEED': 'SPEED_MEAN'}, inplace=True)

    train_data = pd.merge(train_mean_data, train_final_data, left_index=True, right_index=True)
    test_data = pd.merge(test_mean_data, test_final_data, left_index=True, right_index=True)

    return train_data, test_data
