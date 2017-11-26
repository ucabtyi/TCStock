import tushare as ts
import config
import talib
import numpy as np
import matplotlib.pyplot as plt


def get_macd(df, fast, slow, signal):
    fast_d, slow_d, macd_d = talib.MACDEXT(df[config.close_key].values, fastperiod=fast, slowperiod=slow,
                                                       signalperiod=signal, fastmatype=1, slowmatype=1,
                                                       signalmatype=1)
    macd_d *= 2

    df['fast'], df['slow'], df['macd'] = fast_d, slow_d, macd_d
    # df.dropna(how='any')
    df[config.macd_positon_key] = ''
    macd_jincha = df.macd > 0

    df.loc[macd_jincha[np.logical_and(macd_jincha == True, macd_jincha.shift() == False)].index, config.macd_positon_key] = config.jincha
    df.loc[macd_jincha[np.logical_and(macd_jincha == False, macd_jincha.shift() == True)].index, config.macd_positon_key] = config.sicha

    return df


def jincha(df, key, value):
    return (df.loc[df.loc[df[key]==value].index][config.macd_positon_key] == config.jincha).values[0]


def sicha(df, key, value):
    return (df.loc[df.loc[df[key]==value].index][config.macd_positon_key] == config.sicha).values[0]


def fast_gt_0():
    pass


def slow_gt_0():
    pass


def fast_lt_0():
    pass


def slow_lt_0():
    pass

def dibeili():
    pass