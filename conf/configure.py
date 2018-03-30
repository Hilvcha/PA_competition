import os
import sys

module_path=os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

import time
import datetime


class Configure(object):
    base_path=''
    train_data=''
    test_data =''

    # train_data = '/data/dm/train.csv'
    # test_data =  '/data/dm/test.csv'
    # 数据清洗后的路径
    cleaned_path = ''
    # 生成的特征的路径
    features_path = ''
    # 生成的模型可训练和预测的数据集
    datasets_path = ''
    # 最终结果csv存放处
    submit_result_path=''

    #需要merge的特征
    features = {
        #多次行程速度方差的均值
        'speed_variance_mean': {'on': 'TERMINALNO', 'how': 'left'},
    }

if __name__ == '__main__':
    print('========== 当前项目目录 ==========')
    print(Configure.train_data)
    print(Configure.cleaned_path)
    print(Configure.features_path)
    print(Configure.datasets_path)
    print(Configure.submit_result_path)




