# coding: utf-8


def get_label(df):
    df = df[['TERMINALNO', 'Y']].groupby('TERMINALNO', as_index=False).agg(lambda arr: arr.iloc[0])
    return df['Y']
