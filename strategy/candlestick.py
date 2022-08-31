# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a candlestick script file.
"""


import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
from matplotlib.pylab import date2num
import mpl_finance as mpl
import datetime

hs300 = ts.get_hist_data('hs300')
hist_data = hs300[['open', 'close', 'low', 'close', 'volume']]

data_list = []
data_volume = []

for dates, row in hist_data.iterrows():
    # transfer datatime to
    date_time = datetime.datetime.strptime(dates, '%Y-%m-%d')
    # print(dates, date_time)
    t = date2num(date_time)
    print(t)
    open, high, lower, close = row[:4]
    data_list.append((t, open, high, lower, close))
    volume = row[4]
    data_volume.append((t, volume))
    volume = np.array(data_volume)

# 在画板上产生两张子图subplot，并返回，他们共享x轴
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(12, 6))

# 在子图ax1，绘制数据
mpl.candlestick_ohlc(ax1, data_list, width=1.5, colorup='r', colordown='green', alpha=1.0)
ax1.set_title('Hs300 Index')
ax1.set_ylabel('Price')
ax1.grid(True)
ax1.xaxis_date()

plt.bar(volume[:, 0], volume[:, 1] / 10000)
ax2.set_ylabel('volume(wan)')
ax2.grid(True)
ax2.autoscale_view()
# 让x轴label以斜率30来显示
plt.setp(plt.gca().get_xticklabels(), rotation=30)
plt.plot()


