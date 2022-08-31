# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a cointegration script file.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# 平稳的噪声序列
np.random.seed(1234)
x = np.random.normal(0, 1, 1000)
X = pd.Series(x) + 100
# X.plot()


y = np.random.normal(0, 1, 1000)
Y = X + y + 30

for i in range(1000):
    X[i] = X[i] - i/10
    Y[i] = Y[i] - i/10

plt.xlabel('Time')
plt.ylabel('Price')
# X.plot()
# Y.plot()

Z = Y - X
Z.plot()
