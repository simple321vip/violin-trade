# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a bollinger bands script file.
"""
import numpy as np


class KeyChart:
    # 策略作者
    author = 'guan'

    # symbol
    symbol = ''

    # 振幅
    amplitude = ''

    # 峰值, 旧峰值
    apex = ''
    old_apex = ''

    # X-unit
    x = 0

    # 正负, 旧正负
    direction = True
    old_direction = True

    # x-axis, y-axis
    x_axis = []
    y_axis = []

    # 二次突破参数
    apex_1 = ''
    apex_2 = ''

    # 构造方法
    def __init__(self, symbol):
        """
        读取数据库数据
        """
        self.on_read_database(symbol)

        """ 计算振幅 """

        """  """

        print("")

    def on_read_database(self, symbol):
        """
        """
        if True:
            print("")

        data_list = []
        self.compute_amplitude()

        for bar_data in data_list:

            resp = self.compute_apex(bar_data)
            if resp:
                self.on_draw_point()

    def on_bar(self, bar_data):
        """
        """
        resp = self.compute_apex(bar_data)
        if resp:
            self.on_draw_point()

        self.on_signal()

    def compute_apex(self, bar_data):
        """
        compute apex
        while apex is changed, return True
        while apex is unchanged, return False
        default return False
        """
        self.old_apex = self.apex
        self.old_direction = self.direction
        if self.direction:
            if bar_data - self.apex > 0:
                self.apex = bar_data
            elif self.apex - bar_data > self.amplitude:
                self.apex = bar_data
                self.direction = False
                self.x = self.x + 1
            else:
                return False
        else:
            if bar_data - self.apex < 0:
                self.apex = bar_data
            elif bar_data - self.apex > self.amplitude:
                self.apex = bar_data
                self.direction = True
                self.x = self.x + 1
            else:
                return False

        return True

    def on_draw_point(self):
        """
        when direction is changed, add to point
        """
        if self.old_direction != self.direction:
            self.x_axis.append(self.x)
            self.y_axis.append(self.old_apex)

        self.x_axis.append(self.x)
        self.y_axis.append(self.apex)

    def on_signal(self):
        """
        :return:
        """
        self.x_axis.index(self.x - 1)

        print("")

    def compute_amplitude(self):
        """
        :return:
        """
        # nparray = np.array(SZ000625['close'].values)
        # amplitude_list = np.abs(np.diff(nparray))
        # amplitude_mean = np.mean(amplitude_list)
        self.amplitude = ''
