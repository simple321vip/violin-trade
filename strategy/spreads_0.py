# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a corrcoef script file.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ta

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

plt.scatter(df_SZ000725.values, df_SH600026.values)
plt.xlabel(SZ000725)
plt.ylabel(SH600026)

plt.title('Stock price from ' + start + ' to ' + end)
print(SZ000725 + ' and ' + SH600026 + " corrcoef is : " + str(np.corrcoef(df_SZ000725, df_SH600026)[0, 1]))
