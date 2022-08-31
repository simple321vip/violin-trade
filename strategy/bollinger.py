# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a bollinger bands script file.
"""

import tushare as ts
import talib as ta

sh = ts.get_hist_data('sh')
sh = sh.sort_index()

close = sh[['close', 'volume']]
upper, middle, lower = ta.BBANDS(
    sh['close'].values,
    timeperiod=20,
    nbdevup=2,
    nbdevdn=2,
    matype=0
)
close.loc[:, 'upper'] = upper
close.loc[:, 'middle'] = middle
close.loc[:, 'lower'] = lower

close[['close', 'upper', 'middle', 'lower']].plot()
