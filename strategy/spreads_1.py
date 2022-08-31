# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a D-value and stability script file.
"""

import numpy as np
import pandas as pd
import tushare as ta
from statsmodels.tsa.stattools import adfuller

start = '2020-01-01'
end = '2022-01-01'
SZ000725 = '000725'
SH600026 = '600026'

df_SZ000725 = ta.get_hist_data(SZ000725, start, end)[0:200]
df_SH600026 = ta.get_hist_data(SH600026, start, end)[0:200]

# 关于缺失处理
stock = pd.DataFrame()
stock['SZ000725'] = df_SZ000725['close']
stock['SH600026'] = df_SH600026['close']
stock = stock.dropna()
df_SZ000725 = stock['SZ000725']
df_SH600026 = stock['SH600026']

print(SZ000725 + ' and ' + SH600026 + " corrcoef is : " + str(np.corrcoef(df_SZ000725, df_SH600026)[0, 1]))

# 获得 差价
D_value = df_SH600026 - df_SZ000725
D_value.plot()

# 去计算稳定性
adf_test = adfuller(D_value)

result = pd.Series(adf_test[0:4], index=['Test statistic', 'p-value', 'Lags used', 'Number of Observations used'])
for key, value in adf_test[4].items():
    result['Critical Value (%s)' % key] = value
print(result)
