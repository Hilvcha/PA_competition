# coding: utf-8
import time
from functools import wraps
import pandas as pd

def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{}:{} seconds'.format(func.__module__, func.__name__, round(end - start, 2)))
        return r
    return wrapper


# 取得目标向量
def get_label(df):
    df_label = df[['TERMINALNO', 'Y']].groupby('TERMINALNO').first()
    return df_label['Y']


# 时间戳转化
def time_reform(x):
    time_array = time.localtime(x)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_array)


# 对数据按照时间顺序排序
def sort_by_time(train, test):
    train_data = train.sort_values(by='TIME')
    test_data = test.sort_values(by='TIME')
    return train_data, test_data


# 行程方向变化方差
def fun_direction(arr):
    ss = []
    m = (len(arr) - 1)
    try:
        if m == 0:
            return 0
        mean_d = (abs(arr.iloc[-1] - arr.iloc[0]) % 360) / m
        for i in range(len(arr) - 1):
            ss.append(abs(abs(arr.iloc[i + 1] - arr.iloc[i]) % 360 - mean_d))
        return sum(ss) / m
    except:
        return 0


# 统计历史中方向无法获取次数
def fun_direction_none(arr):
    ll = 0
    for i in range(len(arr)):
        if arr.iloc[i] == -1:
            ll += 1
    return ll

#创建空的可以加入类型的df
# df = df_empty(['a', 'b'], dtypes=[np.int64,np.int64,] print list(df.dtypes) # int64, int6
def df_empty(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df
