# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a cointegration script file.
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

# 去计算稳定性
adf_test = adfuller(D_value)

result = pd.Series(adf_test[0:4], index=['Test statistic', 'p-value', 'Lags used', 'Number of Observations used'])
for key, value in adf_test[4].items():
    result['Critical Value (%s)' % key] = value
print(result)

# 均值
mean = np.mean(D_value)
# 标准差
std = np.std(D_value)
up = std + mean
down = mean - std
time = D_value.index
mean_line = pd.Series(mean, index=time)
up_line = pd.Series(up, index=time)
down_line = pd.Series(down, index=time)

result_set = pd.concat([D_value, mean_line, up_line, down_line], axis=1)
result_set.columns = ['spreadprice', 'mean', 'upper', 'down']
result_set.plot(figsize=(10, 5))

print("股票虽然根据相关系数，足够，但是协整性不足，不可以进行套利")
print("简单来说，我们不可以利用这个不收敛价差来进行套利")
