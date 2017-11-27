import tushare as ts
import config
import talib
import numpy as np
import matplotlib.pyplot as plt

def get_ma(df, period=5, key=config.ma5_key):
    df[key] = talib.SMA(df[config.close_key].values, timeperiod=period)
    return df
def jincha(df, index_key, value, fast_key, slow_key):
    index = utils.get_df_index_by_col_value(df, index_key, value)
    pos = df[fast_key] > df[slow_key]
    index_jincha = pos[np.logical_and(pos == True, pos.shift() == False)].index
    return index in index_jincha
