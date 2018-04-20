# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from utils.feature_utils import df_empty

def build_time_features(train_addtime, test_addtime):
    # train_addtime = train
    # test_addtime = test
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
    # 取单独的一个用户组进行综合提取
    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE

    train_user = train_addtime['TERMINALNO'].unique()
    train_data=pd.DataFrame(columns=['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
                           'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],index=train_user)
    # train_data = df_empty(['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
    #                        'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],
    #                       dtypes=[np.int64, np.float32, np.float32, np.float32, np.float32, np.float32, np.float32,
    #                               np.float32, np.int8, np.int8, np.int8],index=train_user)
    for TERMINALNO in train_user:
        user_data = train_addtime.loc[train_addtime['TERMINALNO'] == TERMINALNO]
        # 初始化 时间，方向变化
        tempTime = train_addtime["TIME_STAMP"].iloc[0]
        tempSpeed = train_addtime["SPEED"].iloc[0]
        tempdir = train_addtime["DIRECTION"].iloc[0]
        tempheight = train_addtime["HEIGHT"].iloc[0]

        # 根据时间信息判断最长时间
        maxTime = 0
        maxTimelist = []



        # 用户行驶过程中，打电话危机上升
        phonerisk = 0

        # Direction 突变超过
        dir_risk = 0

        # Height 高度的危险值
        height_risk = 0
        # 时间区间
        Zao = 0
        Wan = 0
        Sheye = 0

        for index, row in user_data.iterrows():

            p_time = row['TIME_hour']
            if 6 <= p_time <= 9:
                Zao = 1
            elif 17 <= p_time <= 19:
                Wan = 1
            elif 0 <= p_time < 6:
                Sheye = 1

            # 如果具有速度，且在打电话
            if tempSpeed > 0 and row["CALLSTATE"] != 4:

                # 人设打电话状态未知情况下，他的危机指数为 0.05
                if row["CALLSTATE"] == 0:
                    phonerisk += math.exp(tempSpeed / 10) * 0.02
                else:
                    phonerisk += math.exp(tempSpeed / 10)

            # 根据时间行驶判断
            if row["TIME_STAMP"] - tempTime == 60:
                maxTime += 60
                tempTime = row["TIME_STAMP"]

                # 判断方向变化程度与具有车速之间的危险系数
                dir_change = (min(abs(row["DIRECTION"] - tempdir), abs(360 + tempdir - row["DIRECTION"])) / 90.0)
                if tempSpeed != 0 and row["SPEED"] > 0:
                    dir_risk += math.pow((row["SPEED"] / 10), dir_change)

                # 海拔变化大的情况下和速度的危险系数
                height_risk += math.pow(abs(row["SPEED"] - tempSpeed) / 10, (abs(row["HEIGHT"] - tempheight) / 100))



                tempheight = row["HEIGHT"]

            elif row["TIME_STAMP"] - tempTime > 60:

                maxTimelist.append(maxTime)
                maxTime = 0
                tempTime = row["TIME_STAMP"]

                tempdir = row["DIRECTION"]
                tempheight = row["HEIGHT"]
                tempSpeed = row["SPEED"]

        speed_max = user_data["SPEED"].max()
        speed_mean = user_data["SPEED"].mean()

        height_mean = user_data["HEIGHT"].mean()

        maxTimelist.append(maxTime)
        maxTime = max(maxTimelist)


        train_data.loc[TERMINALNO] = [TERMINALNO, maxTime, phonerisk, dir_risk, height_risk,speed_max, speed_mean, height_mean,
                                Zao,
                                Wan, Sheye]
    train_data=train_data.astype(float)
    train_data[['TERMINALNO']]=train_data[['TERMINALNO']].astype(int)

    train_data.set_index('TERMINALNO', inplace=True,drop=True)
    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE

    test_user = test_addtime['TERMINALNO'].unique()
    test_data=pd.DataFrame(columns=['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
                           'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],index=test_user)
    # test_data = df_empty(['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
    #                        'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],
    #                       dtypes=[np.int64, np.float32, np.float32, np.float32, np.float32, np.float32, np.float32,
    #                               np.float32, np.int8, np.int8, np.int8],index=test_user)
    for TERMINALNO in test_user:
        user_data = test_addtime.loc[test_addtime['TERMINALNO'] == TERMINALNO]
        # 初始化 时间，方向变化
        tempTime = test_addtime["TIME_STAMP"].iloc[0]
        tempSpeed = test_addtime["SPEED"].iloc[0]
        tempdir = test_addtime["DIRECTION"].iloc[0]
        tempheight = test_addtime["HEIGHT"].iloc[0]

        # 根据时间信息判断最长时间
        maxTime = 0
        maxTimelist = []



        # 用户行驶过程中，打电话危机上升
        phonerisk = 0

        # Direction 突变超过
        dir_risk = 0

        # Height 高度的危险值
        height_risk = 0
        # 时间区间
        Zao = 0
        Wan = 0
        Sheye = 0

        for index, row in user_data.iterrows():

            p_time = row['TIME_hour']
            if 6 <= p_time <= 9:
                Zao = 1
            elif 17 <= p_time <= 19:
                Wan = 1
            elif 0 <= p_time < 6:
                Sheye = 1

            # 如果具有速度，且在打电话
            if tempSpeed > 0 and row["CALLSTATE"] != 4:

                # 人设打电话状态未知情况下，他的危机指数为 0.05
                if row["CALLSTATE"] == 0:
                    phonerisk += math.exp(tempSpeed / 10) * 0.02
                else:
                    phonerisk += math.exp(tempSpeed / 10)

            # 根据时间行驶判断
            if row["TIME_STAMP"] - tempTime == 60:
                maxTime += 60
                tempTime = row["TIME_STAMP"]

                # 判断方向变化程度与具有车速之间的危险系数
                dir_change = (min(abs(row["DIRECTION"] - tempdir), abs(360 + tempdir - row["DIRECTION"])) / 90.0)
                if tempSpeed != 0 and row["SPEED"] > 0:
                    dir_risk += math.pow((row["SPEED"] / 10), dir_change)

                # 海拔变化大的情况下和速度的危险系数
                height_risk += math.pow(abs(row["SPEED"] - tempSpeed) / 10, (abs(row["HEIGHT"] - tempheight) / 100))



                tempheight = row["HEIGHT"]

            elif row["TIME_STAMP"] - tempTime > 60:

                maxTimelist.append(maxTime)
                maxTime = 0
                tempTime = row["TIME_STAMP"]

                tempdir = row["DIRECTION"]
                tempheight = row["HEIGHT"]
                tempSpeed = row["SPEED"]

        speed_max = user_data["SPEED"].max()
        speed_mean = user_data["SPEED"].mean()

        height_mean = user_data["HEIGHT"].mean()

        maxTimelist.append(maxTime)
        maxTime = max(maxTimelist)


        test_data.loc[TERMINALNO] = [TERMINALNO, maxTime, phonerisk, dir_risk, height_risk,speed_max, speed_mean, height_mean,
                                Zao,
                                Wan, Sheye]
    test_data=test_data.astype(float)
    test_data[['TERMINALNO']]=test_data[['TERMINALNO']].astype(int)

    test_data.set_index('TERMINALNO', inplace=True,drop=True)
    return train_data,test_data






    #
    # test_addtime['TIME_is_weekend'] = test_addtime['TIME_weekday'].map(lambda d: 1 if (d == 0) | (d == 6)else 0)
    # test_addtime['TIME_week_hour'] = test_addtime['TIME_weekday'] * 24 + test_addtime['TIME_hour']
    #
    # train_weekend=train_addtime[['TERMINALNO','TRIP_ID','TIME_is_weekend']].groupby(['TERMINALNO', 'TRIP_ID'],
    #                                                            as_index=False).agg(lambda x: np.mean(pd.Series.mode(x)))
    # train_weekend=train_weekend[['TERMINALNO','TIME_is_weekend']].groupby(['TERMINALNO'],
    #                                                            as_index=True).mean()
    # test_weekend = test_addtime[['TERMINALNO', 'TRIP_ID', 'TIME_is_weekend']].groupby(['TERMINALNO', 'TRIP_ID'],
    #                                                                                     as_index=False).agg(
    #     lambda x: np.mean(pd.Series.mode(x)))
    # test_weekend = test_weekend[['TERMINALNO', 'TIME_is_weekend']].groupby(['TERMINALNO'],
    #                                                                          as_index=True).mean()
    #
    #
    # return train_weekend,test_weekend
