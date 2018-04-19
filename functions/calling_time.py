# coding: utf-8
# created by cjr
import pandas as pd


def get_calling_time(df):
    time1 = pd.Timestamp(0)
    now_idx = 0

    for i in range(df.shape[0]):
        if df.iloc[i, 3] == 0 or df.iloc[i, 3] == 1:  # calling state
            time1 = df.iloc[i, 4]
            now_idx = i
            break
    if time1 == pd.Timestamp(0):
        return pd.Timedelta("0")

    time2 = pd.Timestamp(0)
    for i in range(now_idx, df.shape[0]):
        if df.loc(i, 3) == 4:  # calling state
            time2 = df.iloc(i, 4)
            break
    if time2 == pd.Timestamp(0):
        time2 = df.loc(df.shape[0], 4)
    # calculate distance between time1 and time2
    return time2 - time1


def calling_time(train, test):
    """
        通话时间(在总行程时间中的占比)
    """
    print(train)
    train_data = train[['TERMINALNO', 'TRIP_ID', 'CALLSTATE', 'TIME']].groupby(["TERMINALNO", "TRIP_ID"]).apply(
        get_calling_time)
    print(train_data)
    train_series = train_data.groupby("TERMINALNO").sum().apply(lambda x: x.total_seconds())
    train_res = pd.DataFrame(train_series, columns=["calling_time"])
    print(train_series)


    test_data = test[['TERMINALNO', 'TRIP_ID', 'CALLSTATE', 'TIME']].groupby(["TERMINALNO", "TRIP_ID"]).apply(
        get_calling_time)
    test_series = test_data.groupby("TERMINALNO").sum().apply(lambda x: x.total_seconds())
    test_res = pd.DataFrame(test_series, columns=["calling_time"])
    return train_res, test_res
