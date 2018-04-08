# coding : utf-8
# created by wyj


def speed_variance_mean(train, test):
    train_data = train[['TERMINALNO', 'TRIP_ID', 'SPEED']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).var()
    train_data = train_data[['TERMINALNO', 'SPEED']].groupby('TERMINALNO', as_index=True).mean()

    test_data = test[['TERMINALNO', 'TRIP_ID', 'SPEED']].groupby(['TERMINALNO', 'TRIP_ID'], as_index=False).var()
    test_data = test_data[['TERMINALNO', 'SPEED']].groupby('TERMINALNO', as_index=True).mean()
    train_data = train_data.rename(columns={'SPEED': 'SPEED_VAR_MEAN'})
    test_data = test_data.rename(columns={'SPEED': 'SPEED_VAR_MEAN'})

    return train_data, test_data
