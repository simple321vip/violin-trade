import pandas as pd
import tushare as ts
import talib as ta
import numpy as np

sh = ts.get_hist_data('sh')
sh = sh.sort_index()



