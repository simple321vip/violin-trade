# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a simple moving average script file.
"""

import pandas as pd
import tushare as ts
import talib as ta


sh = ts.get_hist_data('sh')
sh = sh.sort_index()

# 1. conpare SMA to MA, the result is that SMA=MA
sma = ta.SMA(sh['close'].values, 20)
ma = ta.MA(sh['close'].values, 20)

pd.DataFrame(sma).plot()
pd.DataFrame(ma).plot()
