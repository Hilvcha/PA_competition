# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from utils.feature_utils import df_empty


def build_time_features(data):
    # train_addtime = train
    # test_addtime = test
    data['TIME_year'] = data['TIME'].dt.year
    data['TIME_month'] = data['TIME'].dt.month
    data['TIME_day'] = data['TIME'].dt.day
    data['TIME_weekofyear'] = data['TIME'].dt.weekofyear
    data['TIME_hour'] = data['TIME'].dt.hour
    data['TIME_minute'] = data['TIME'].dt.minute
    data['TIME_weekday'] = data['TIME'].dt.weekday
    data['TIME_is_weekend'] = data['TIME_weekday'].map(lambda d: 1 if (d == 0) | (d == 6) else 0)
    data['TIME_week_hour'] = data['TIME_weekday'] * 24 + data['TIME_hour']

    # 取单独的一个用户组进行综合提取
    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE

    train_user = data['TERMINALNO'].unique()
    train_data = pd.DataFrame(columns=['TERMINALNO', 'call_risk', 'dir_risk', 'height_risk', 'time_max', 'speed_max',
                                       'speed_mean', 'height_mean', 'am', 'pm', 'all_night', ], index=train_user)
    # train_data = df_empty(['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
    #                        'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],
    #                       dtypes=[np.int64, np.float32, np.float32, np.float32, np.float32, np.float32, np.float32,
    #                               np.float32, np.int8, np.int8, np.int8],index=train_user)
    for TERMINALNO in train_user:
        user_data = data.loc[data['TERMINALNO'] == TERMINALNO]
        tempTime = data["TIME_STAMP"].iloc[0]
        tempSpeed = data["SPEED"].iloc[0]
        tempDir = data["DIRECTION"].iloc[0]
        tempHeight = data["HEIGHT"].iloc[0]

        # 每段行程总时间
        time_max = 0
        time_maxlist = []

        # 通话危险随速度上升
        call_risk = 0

        # Direction 突变超过
        dir_risk = 0

        # Height 高度的危险值
        height_risk = 0
        # 时间区间
        am = 0
        pm = 0
        night = 0

        for index, row in user_data.iterrows():

            p_time = row['TIME_hour']
            if 6 <= p_time <= 9:
                am += 1
            elif 17 <= p_time <= 19:
                pm += 1
            elif 0 <= p_time < 6:
                night += 1

                # 如果具有速度，且在打电话
            if tempSpeed > 0 and row["CALLSTATE"] != 4:

                # 人设打电话状态未知情况下，他的危机指数为 0.05
                if row["CALLSTATE"] == 0:
                    call_risk += math.exp(tempSpeed / 10) * 0.02
                else:
                    call_risk += math.exp(tempSpeed / 10)

                # 根据时间行驶判断
            if row["TIME_STAMP"] - tempTime == 60:
                time_max += 60
                tempTime = row["TIME_STAMP"]

                # 判断方向变化程度与具有车速之间的危险系数
                dir_change = (min(abs(row["DIRECTION"] - tempDir), abs(360 + tempDir - row["DIRECTION"])) / 90.0)
                if tempSpeed != 0 and row["SPEED"] > 0:
                    dir_risk += math.pow((row["SPEED"] / 10), dir_change)

                    # 海拔变化大的情况下和速度的危险系数
                    height_risk += math.pow(abs(row["SPEED"] - tempSpeed) / 10, (abs(row["HEIGHT"] - tempHeight) / 100))

                tempDir = row['DIRECTION']
                tempHeight = row["HEIGHT"]

            elif row["TIME_STAMP"] - tempTime > 60:

                time_maxlist.append(time_max)
                time_max = 0
                tempTime = row["TIME_STAMP"]

                tempDir = row["DIRECTION"]
                tempHeight = row["HEIGHT"]
                tempSpeed = row["SPEED"]

        speed_max = user_data["SPEED"].max()
        speed_mean = user_data["SPEED"].mean()

        height_mean = user_data["HEIGHT"].mean()

        time_maxlist.append(time_max)
        time_max = max(time_maxlist)

        time_cout = len(user_data)
        am = am / time_cout
        pm = pm / time_cout
        night = night / time_cout

        longitude_mean = user_data['LONGITUDE'].mean()
        longitude_var = user_data['LONGITUDE'].agg(np.var)
        longitude_span = user_data['LONGITUDE'].max() - user_data['LONGITUDE'].min()
        latitude_mean = user_data['LATITUDE'].mean()
        latitude_var = user_data['LATITUDE'].agg(np.var)
        latitude_span = user_data['LATITUDE'].max() - user_data['LATITUDE'].min()

        weekend = user_data['TIME_is_weekend'].mean()
        train_data.loc[TERMINALNO] = [TERMINALNO, call_risk, dir_risk, height_risk, time_max, speed_max, speed_mean,
                                      height_mean,
                                      am,
                                      pm, night, ]
    train_data = train_data.astype(float)
    train_data[['TERMINALNO']] = train_data[['TERMINALNO']].astype(int)

    train_data.set_index('TERMINALNO', inplace=True, drop=True)
    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE

    return train_data
