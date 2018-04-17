# coding : utf-8
# created by wyj
import pandas as pd


def mean(x):
    return sum(x) / len(x)


def trip_id_interval_mean(train, test):
    """
    用户多次行程时间间隔的平均数
    :param train:
    :param test:
    :return:
    """
    td1 = train[["TIME", "TERMINALNO", "TRIP_ID"]].groupby(['TERMINALNO'])
    tmp = []
    for i, value in td1:  # for each user
        max_values = value.groupby(['TRIP_ID']).max().sort_values(by="TIME")
        min_values = value.groupby(['TRIP_ID']).min().sort_values(by="TIME")
        # for maxv, minv in zip(max_values.index, min_values.index):
        #     if maxv != minv:
        #         print('========================ERROR=========================================')
        # # if i == 1:
        # #     print(max_values)
        # #     for maxv, minv in zip(max_values.index, min_values.index):
        # #         print(max_values.loc[maxv], maxv)
        # #         print(min_values.loc[minv], minv)

        if min_values.shape[0] != 1:
            interval = min_values["TIME"].values[1:] - max_values["TIME"].values[:-1]
            # if i == 1:
            #     print(interval)
            tmp.append(mean(interval))
        else:
            tmp.append(0)
    # fill na:
    mean_tmp = mean(tmp)
    tmp = [x if x != 0 else mean_tmp for x in tmp]
    # transfer to DataFrame:
    train_data = pd.DataFrame(tmp, index=[i + 1 for i in range(len(tmp))])
    train_data.rename(columns={0: "INTERVAL_MEAN"}, inplace=True)
    train_data.rename_axis("TERMINALNO", inplace=True)

    tmp = []
    # test data
    td1 = test[["TIME", "TERMINALNO", "TRIP_ID"]].groupby(['TERMINALNO'])
    for i, value in td1:  # for each user
        max_values = value.groupby(['TRIP_ID']).max().sort_values(by="TIME")
        min_values = value.groupby(['TRIP_ID']).min().sort_values(by="TIME")
        if min_values.shape[0] != 1:
            interval = min_values["TIME"].values[1:] - max_values["TIME"].values[:-1]
            tmp.append(mean(interval))
        else:
            tmp.append(0)
    # fill na:
    mean_tmp = mean(tmp)
    tmp = [x if x != 0 else mean_tmp for x in tmp]
    # transfer to DataFrame:
    test_data = pd.DataFrame(tmp, index=[i + 1 for i in range(len(tmp))])
    test_data.rename(columns={0: "INTERVAL_MEAN"}, inplace=True)
    test_data.rename_axis("TERMINALNO", inplace=True)

    return train_data, test_data
