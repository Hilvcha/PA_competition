# coding : utf-8
# created by wyj
import numpy as np
import pandas as pd
import math
from math import radians, cos, sin, asin, sqrt

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
                                       'speed_mean', 'height_mean', 'am', 'pm', 'all_night',
                                       ], index=train_user)
    # train_data = df_empty(['TERMINALNO', 'maxTime', 'phonerisk', 'dir_risk', 'height_risk', 'speed_max',
    #                        'speed_mean', 'height_mean', 'Zao', 'Wan', 'Sheye'],
    #                       dtypes=[np.int64, np.float32, np.float32, np.float32, np.float32, np.float32, np.float32,
    #                               np.float32, np.int8, np.int8, np.int8],index=train_user)
    for TERMINALNO in train_user:
        user_data = data.loc[data['TERMINALNO'] == TERMINALNO]

        user_data['DIRECTION'].replace(-1,user_data["DIRECTION"].mean(),inplace=True)
        user_data['SPEED'].replace(-1,user_data["SPEED"].mean(),inplace=True)


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

        record_cout = user_data.shape[0]
        am = am / record_cout
        pm = pm / record_cout
        night = night / record_cout

        longitude_mean = user_data['LONGITUDE'].mean()
        longitude_var = user_data['LONGITUDE'].agg(np.var)
        longitude_span = user_data['LONGITUDE'].max() - user_data['LONGITUDE'].min()
        latitude_mean = user_data['LATITUDE'].mean()
        latitude_var = user_data['LATITUDE'].agg(np.var)
        latitude_span = user_data['LATITUDE'].max() - user_data['LATITUDE'].min()

        # 各种通话状态占比
        call_0 = user_data.loc[user_data['CALLSTATE'] == 0].shape[0] / float(record_cout)
        call_1 = user_data.loc[user_data['CALLSTATE'] == 1].shape[0] / float(record_cout)
        call_2 = user_data.loc[user_data['CALLSTATE'] == 2].shape[0] / float(record_cout)
        call_3 = user_data.loc[user_data['CALLSTATE'] == 3].shape[0] / float(record_cout)
        call_4 = user_data.loc[user_data['CALLSTATE'] == 4].shape[0] / float(record_cout)

        # 地点特征
        startlong = user_data['LONGITUDE'].iloc[0]
        startlat = user_data['LATITUDE'].iloc[0]
        hdis1 = haversine1(startlong, startlat, 113.9177317, 22.54334333)  # 距离某一点的距离
        if 'Y' in data.columns:
            target=user_data['Y'].iloc[0]
        else:
            target=np.nan

        weekend = user_data['TIME_is_weekend'].mean()

        train_data.loc[TERMINALNO] = [TERMINALNO, call_risk, dir_risk, height_risk, time_max, speed_max, speed_mean,
                                      height_mean,am, pm, night,
                                     ]
    train_data = train_data.astype(float)
    train_data[['TERMINALNO']] = train_data[['TERMINALNO']].astype(int)

    train_data.set_index('TERMINALNO', inplace=True, drop=True)
    # TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE

    return train_data

def haversine1(lon1, lat1, lon2, lat2):  # 经度 1，纬度 1，经度 2，纬度 2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000
