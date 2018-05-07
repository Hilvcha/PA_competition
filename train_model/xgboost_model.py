# coding: utf-8
import os
import sys

module_path = os.path.abspath(os.path.join('..'))
sys.path.append(module_path)

from utils.feature_utils import time_this
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import xgboost as xgb
from train_model.get_datasets import merge_datasets
from conf.configure import Configure
from sklearn.model_selection import GridSearchCV



@time_this
def xgboost_train(train_set, test_set, slices):
    train, test, train_label, test_index = merge_datasets(train_set, test_set, slices)
    print(train.head(5))
    user_id = test.pop('TERMINALNO')
    train.drop(['TERMINALNO'], axis=1, inplace=True)
    # print('train.', train.axes)
    # print(train.dtypes)
    print(train_label.shape, train.shape)
    param = {
        'learning_rate': 0.1,
        'n_estimators': 1000,
        'max_depth': 4,
        'min_child_weight': 2,
        'gamma': 0,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'eta': 0.05,
        'silent': 1,
        # 'objective': 'binary:logistic',
        'eval_metric': 'auc'
    }

    num_round = 100
    useTrainCV = 0
    cv_folds = 5

    if useTrainCV == 0:
        # 简单交叉验证
        x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)

        d_train = xgb.DMatrix(x_train, label=y_train)
        # print(d_train)
        d_val = xgb.DMatrix(x_val, label=y_val)

        eval_list = [(d_val,'v'), (d_train,'t')]
        bst = xgb.train(param, d_train, num_round, eval_list, early_stopping_rounds=100)
        d_test = xgb.DMatrix(test)
        prediction = bst.predict(d_test)

    elif useTrainCV == 1:
        # 使用xgboost的cv(二分类)
        # clf = xgb.XGBClassifier(**param,)
        train_label=train_label.map(lambda x:0 if (x == 0)  else 1)
        x_train, x_val, y_train, y_val = train_test_split(train, train_label, test_size=0.3, random_state=100)
        d_train = xgb.DMatrix(x_train, label=y_train)
        d_val = xgb.DMatrix(x_val, label=y_val)

        eval_list = [(d_val,'v'), (d_train,'t')]
        bst = xgb.train(param, d_train, num_round, eval_list, early_stopping_rounds=100)

        d_test = xgb.DMatrix(test)
        prediction = bst.predict(d_test)
        for i in range(len(train.columns)):
            print('{0}:{1}'.format(train.columns[i], bst.feature_importances_[i]))
        # prediction = bst.predict(test)
        prediction = bst.predict_proba(test)[:,1]
    elif useTrainCV == 2:
       # sklearn网格搜索
       ####  模型优化    cross-validation+grid search    ####
        # X_train, X_test, y_train, y_test = train_test_split(train, train_label, test_size=0.3,
        #                                                     random_state=100)
        # 构建参数组合
        param_grid = {
            'max_depth': range(3, 10, 2),
            'min_child_weight': range(2, 10, 2)
        }
        grid_search = GridSearchCV(xgb.XGBRegressor(**param), param_grid,cv=5)
        grid_search.fit(train, train_label)
        results = pd.DataFrame(grid_search.cv_results_)

        best = np.argmax(results.mean_test_score.values)
        print("Best parameters: {}".format(grid_search.best_params_))
        print("Best cross-validation score: {:.5f}".format(grid_search.best_score_))
        print("Best estimator:\n{}".format(
            grid_search.best_estimator_))
        prediction = grid_search.predict(test)


    pred_arr = np.array(prediction)
    pred_series = pd.Series(pred_arr, name='Pred', index=test_index)
    submit_df = pd.concat([user_id, pred_series], axis=1)
    # print(submit_df)

    submit_df.rename(columns={'TERMINALNO': 'Id'}, inplace=True)
    # print(submit_df)
    submit_df.to_csv(path_or_buf=Configure.submit_result_path, sep=',', index=None)


if __name__ == '__main__':
    print('========== xgboost 模型训练 ==========')
    # model_train()
# 日志详情
# *****section 2 ******
# functions.functions.save_all_features:1505.19 seconds
# *****section 3 ****** functions.functions.save_all_features:1476.56 seconds
# *****section 4 ****** functions.functions.save_all_features:1500.83 seconds
# *****section 5 ****** functions.functions.save_all_features:1540.52 seconds
# *****section 6 ****** functions.functions.save_all_features:1593.36 seconds
# *****section 7 ****** functions.functions.save_all_features:1503.79 seconds
# *****section 8 ****** functions.functions.save_all_features:1480.98 seconds
# *****section 9 ****** functions.functions.save_all_features:1504.11 seconds
# pd merge height Index(['MAX_SUCC_INC', 'MEAN_SUCC_INC', 'VAR_SUCC_INC', 'HEIGHT_RISK', 'DIRECTION_RISK', 'CALLSTATE_RISK'], dtype='object')
# (16726, 6) (14045, 6)
# (16727, 7) (14046, 7) (16727, 1) (14046,)
#     TERMINALNO MAX_SUCC_INC MEAN_SUCC_INC VAR_SUCC_INC HEIGHT_RISK DIRECTION_RISK CALLSTATE_RISK
# TERMINALNO
# 0   0           NaN         NaN             NaN        NaN          NaN             NaN
# 1   1           40.0        4.000000        50.105263   8.922499    9.364827        1.500574
# 2   2           30.0        5.480769        64.931665  5.574673     6.081244        0.456873
# Traceback (most recent call last): File "/data/share/jingsuan/js_project/1825122858_1825122858/_PA_competition/main.py", line 37, in <module> liner_train(trainSet,testSet,slices) File "/data/share/jingsuan/js_project/1825122858_1825122858/_PA_competition/utils/feature_utils.py", line 10, in wrapper r = func(*args, **kwargs) File "/data/share/jingsuan/js_project/1825122858_1825122858/_PA_competition/train_model/liner_model.py", line 31, in liner_train linreg.fit(train, train_label) File "/usr/local/python3/lib/python3.6/site-packages/sklearn/linear_model/ridge.py", line 665, in fit return super(Ridge, self).fit(X, y, sample_weight=sample_weight) File "/usr/local/python3/lib/python3.6/site-packages/sklearn/linear_model/ridge.py", line 483, in fit multi_output=True, y_numeric=True) File "/usr/local/python3/lib/python3.6/site-packages/sklearn/utils/validation.py", line 573, in check_X_y ensure_min_features, warn_on_dtype, estimator) File "/usr/local/python3/lib/python3.6/site-packages/sklearn/utils/validation.py", line 453, in check_array _assert_all_finite(array)
# File "/usr/local/python3/lib/python3.6/site-packages/sklearn/utils/validation.py", line 44, in _assert_all_finite "or a value too large for %r." % X.dtype) ValueError: Input contains NaN, infinity or a value too large for dtype('float64').
