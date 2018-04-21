# coding: utf-8
import os
import sys
import time

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

# TERMINALNO, TIME, TRIP_ID, LONGITUDE, LATITUDE, DIRECTION, HEIGHT, SPEED, CALLSTATE, Y

from conf.configure import Configure
from utils.data_utils import save_features
from utils.feature_utils import time_this

from functions.trip_id_count import trip_id_count
from functions.trip_id_interval_mean import trip_id_interval_mean
from functions.speed_variance_mean import speed_variance_mean
from functions.speed_final_mean import speed_final_mean
from functions.time_direction_change_feat import time_gap_direction_change_feat
from functions.callstate_feat import callstate_feat
from functions.calling_time import calling_time
from functions.time import  build_time_features
from functions.height import height_feet


@time_this
def save_all_features(train, test,s):
    funcs = {
        'speed_variance_mean': speed_variance_mean,
        'trip_id_count': trip_id_count,
        'trip_id_interval_mean': trip_id_interval_mean,
        'speed_final_mean': speed_final_mean,
        'time_gap_direction_change_feat': time_gap_direction_change_feat,
        # 通话时间(在总行程时间中的占比)
        "calling_time": calling_time,
        'callstate_feat': callstate_feat,
        "build_time_features": build_time_features,
        "height":height_feet,
    }
    for feat_name in Configure.features:
        save_features(funcs[feat_name](train),'train', feat_name,s)
        save_features(funcs[feat_name](test),'test', feat_name,s)



if __name__ == "__main__":
    print("****************** feature **********************")
    # 程序入口
    # save_all_features()
