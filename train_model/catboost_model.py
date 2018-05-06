# # coding: utf-8
# import os
# import sys
#
# module_path = os.path.abspath(os.path.join('..'))
# sys.path.append(module_path)
#
# from utils.feature_utils import time_this
# from sklearn.model_selection import train_test_split
# import numpy as np
# import pandas as pd
# import xgboost as xgb
# import lightgbm as lgb
# import catboost as cat
# from train_model.get_datasets import merge_datasets
# from conf.configure import Configure
#
#
# @time_this
# def cat_train(train_set, test_set, slices):
#     train, test, train_label, test_index = merge_datasets(train_set, test_set, slices)
#     print(train.head(5))
#     user_id = test.pop('TERMINALNO')
#     train.drop(['TERMINALNO'], axis=1, inplace=True)
#     # print('train.', train.axes)
#     # print(train.dtypes)
#     print(train_label.shape, train.shape)
#     x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)
#
#     model = cat.CatBoostRegressor(iterations=200, depth=3, learning_rate=0.1, loss_function='RMSE', eval_metric="AUC",
#                                   verbose=False,)
#     model.fit(x_train, y_train, eval_set=(x_val, y_val), plot=True)
#     prediction = model.predict(test)
#
#     # train_data = lgb.Dataset(x_train, label=y_train)
#     # eval_data = lgb.Dataset(x_val, label=y_val)
#     # learning_rate = 0.1
#     # num_leaves = 15
#     # min_data_in_leaf = 2000
#     # feature_fraction = 0.6
#     # num_boost_round = 10000
#     # param = {
#     #     "objective": "regression",
#     #     "boosting_type": "gbdt",
#     #     "learning_rate": 0.01,
#     #     'metric': 'auc',
#     #     "feature_fraction": 0.6,
#     #     "verbosity": -1,
#     #     "min_child_samples": 10,
#     #     "subsample": 0.9,
#     #     "num_leaves": 8,
#     #
#     # }
#     # watchlist=[train_data,eval_data]
#     # num_round = 200
#     # bst = lgb.train(param, train_data, num_round, valid_sets=watchlist,early_stopping_rounds=100,)
#     # prediction = bst.predict(test)
#     # 这里会否有更好的拼接方式？
#     pred_arr = np.array(prediction)
#     pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
#     submit_df = pd.concat([user_id, pred_series], axis=1)
#     # print(submit_df)
#
#     submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
#     # print(submit_df)
#     submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)
#
#
# if __name__ == '__main__':
#     print('========== catboost 模型训练 ==========')
