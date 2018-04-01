# coding: utf-8


def get_label(df):
    df_label = df[['TERMINALNO', 'Y']].groupby('TERMINALNO').agg(lambda arr: arr.iloc[0])
    return df_label
