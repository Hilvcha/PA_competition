# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from utils.feature_utils import time_this
from sklearn.model_selection import train_test_split

import lightgbm as lgb


@time_this
def lgb_train(train, train_label, test):

    x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)

    train_data = lgb.Dataset(x_train, label=y_train.ravel())
    test_data1 = lgb.Dataset(x_val, label=y_val.ravel())


    param = {'num_leaves': 31,
             'num_trees': 33,
             'metric': 'rmse',
             'is_unbalance': 'true',
             'verbose':-1,
            }

    num_round = 10
    bst = lgb.train(param, train_data, num_round, valid_sets=test_data1)
    prediction = bst.predict(test)

    return prediction
    # submit_df = pd.concat([user_id, pred_series], axis=1)
    # # print(submit_df)
    #
    # submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # # print(submit_df)
    # submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)



if __name__ == '__main__':
    print('========== lgb 模型训练 ==========')
    # model_train()
