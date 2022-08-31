import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
spread = 3

hs300 = ts.get_hist_data("hs300")
hs300['short'] = np.round(hs300.rolling(window=3).mean(), 2)
hs300['long'] = np.round(hs300.rolling(window=3).mean(), 2)
hs300['short-long'] = hs300['short'] - hs300['long']

hs300[['close', 'short', 'long']].plot()

# hs300['close'].plot()
