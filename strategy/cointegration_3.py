# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a cointegration script file.
"""

import numpy as np
import pandas as pd
import tushare as ts
import statsmodels.api as sm


def find_cointegration_pairs(dataframe):
    # to obtain the length of dataframe
    n = dataframe.shape[1]
    # initialize the matrix of p-value
    pvalue_matrix = np.ones((n, n))
    # to obtain column name
    keys = dataframe.keys()
    # initialize the array of cointegration
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            stock1 = dataframe[keys[i]]
            stock2 = dataframe[keys[j]]
            result = sm.tsa.stattools.coint(stock1, stock2)
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j], pvalue))
    return pvalue_matrix, pairs


stock = pd.DataFrame()
stock_list = ['601169', '600036']
df = ts.get_k_data(stock_list[0])[['date', 'close']].set_index('date')
df.columns = [stock_list[0]]

for z in stock_list[1:]:
    ds = ts.get_k_data(z)[['date', 'close']].set_index('date')
    ds.columns = [z]
    df = df.merge(ds, right_index=True, left_index=True)

# obtain matrix, pair
pvalues, stock_pairs = find_cointegration_pairs(df)

stock_601169 = df['601169']
stock_600036 = df['600036']

X = sm.add_constant(stock_601169)
result = (sm.OLS(stock_600036, stock_601169)).fit()
print(result.summary())

D_value = stock_600036 - 9.9568 * stock_601169
mean = np.mean(D_value)
std = np.std(D_value)
up = mean + std
down = mean - std
time = D_value.index
mean_line = pd.Series(mean, index=time)
up_line = pd.Series(up, index=time)
down_line = pd.Series(down, index=time)
set_list = pd.concat([D_value, mean_line, up_line, down_line], axis=1)
set_list.plot()
