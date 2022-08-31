# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a corrcoef script file.
"""

import numpy as np
import matplotlib.pyplot as plt

X = np.random.random(50)
Y = X + np.random.normal(0, 0.1, 50)

plt.scatter(X, Y)
plt.xlabel('X value')
plt.ylabel('Y value')

type(np.corrcoef(X, Y))
# corrcoef 返回 相关系数矩阵， [0, 1] 第1行第二列的数据
print('相关系数: ' + str(np.corrcoef(X, Y)[0, 1]))
