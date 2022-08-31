import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from datetime import date

# token = '6d70e32a299e658d38d5acb7128192c71e33dbbc0c2de2cc219e2817'
# pro = ts.pro_api(token)

# xxx = ts.get_czce_daily()
# df = pro.trade_cal(exchange='CZCE', start_date='20180101', end_date='20181231')
hs300 = ts.get_hist_data("hs300")

# <class 'pandas.core.frame.DataFrame'>
print(type(hs300))

# <class 'pandas.core.series.Series'>
print(type(hs300['close']))

# head
print(hs300.head(5))

# tail
print(hs300.tail(5))

# sort <default> axis = 0
hs300 = hs300.sort_index()

# columns index
print(hs300.columns)

# column data
print(hs300['close'])

#
print(hs300[hs300.index=='2020-03-03'])

