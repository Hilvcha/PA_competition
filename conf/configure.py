# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)


class Configure(object):
    base_path = os.path.abspath(os.path.join(__file__, '../..'))
    train_path = os.path.join(base_path, "train.csv")
    test_path = os.path.join(base_path, "test.csv")

    # 数据清洗后的路径
    cleaned_path = os.path.join(base_path, 'cleaned')
    # 生成的特征的路径
    features_path = os.path.join(base_path, 'features')
    # 生成的模型可训练和预测的数据集
    datasets_path = os.path.join(base_path, 'datasets')
    # 最终结果csv存放处
    submit_result_path = os.path.abspath(os.path.join(base_path, 'model', 'submit.csv'))
    # 需要merge的特征
    features = [

        # 用户多次行程时间间隔的平均数
        # 'trip_id_interval_mean',

        # 通话时间(在总行程时间中的占比)
        # "calling_time",bug
        # # time
         "build_time_features",
    #     # # 每名用户的行程数
    #     'trip_id_count',
    #     # # 用户最后一次行程速度的平均数
    #     'speed_final_mean',
    #     # # 多次行程速度方差的均值
    #     'speed_variance_mean',
    #     # # 行程时间差&中行程方向变化方差&方向无法获取次数
    #     'time_gap_direction_change_feat',
    #     # # 通话状态
    #     'callstate_feat',
        # height最大连续子数组
        # "height",
    ]


if __name__ == '__main__':
    print('========== 当前项目目录 ==========')
    print(Configure.train_path)
    print(Configure.cleaned_path)
    print(Configure.features_path)
    print(Configure.datasets_path)
    print(Configure.submit_result_path)
