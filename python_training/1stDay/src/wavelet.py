# -*- coding: utf-8 -*-
# wavelet.py
# 2014.10.26 K. Kuwata

from numpy import median, sqrt
from numpy.core.umath import absolute, floor, log
from matplotlib import pyplot as plt
import datetime as dt
import pywt
import jsm


class wavelet_jsm:
    def __init__(self, code, year):
        self.code = code
        self.year = year

    def GetStockValue(self):
        q = jsm.Quotes()
        start = dt.date(self.year, 1, 1)
        end = dt.date(self.year, 12, 31)
        stocks = q.get_historical_prices(self.code, jsm.DAILY, start, end)
        dates = [data.date for data in stocks]
        value = [data.close for data in stocks]
        return dates, value

    def denoise(self, data):
        wavelet = pywt.wavelist()[18]
        noiseSigma = median(absolute(data - median(data))) / 0.6745
        levels = int(floor(log(len(data))))
        WC = pywt.wavedec(data, wavelet, level=levels)
        threshold = noiseSigma * sqrt(2 * log(len(data)))
        NWC = map(lambda x: pywt.thresholding.hard(x, threshold), WC)
        return pywt.waverec(NWC, wavelet)[1:]

    def graph_smooth(self, x, y, sy):
        lab = "Securities code:%s" % (self.code)
        plt.plot(x, y, color="red", linestyle="-", label=lab)
        plt.plot(x, sy, color='blue', linestyle="--", label="Wavelet")
        plt.xticks(rotation=30)
        title = "Stock value (SC:%s) in %s" % (self.code, self.year)
        plt.suptitle(title, size='20')
        plt.legend(loc='upper left', fontsize=10)
        plt.show()

