# -*- coding: utf-8 -*-
# 2014.09.06 K. Kuwata
# EVI-Wavelet.py
"""
    MODISのEVIをWaveletでノイズ除去及びスムージングし、フェノロジーを推定する
"""

from osgeo import gdal
from osgeo.gdalconst import *

import numpy
from numpy import median, sqrt
import pywt

from numpy.core.umath import absolute, floor, log
from datetime import datetime as dt

from scipy.interpolate import splrep, splev

class MOD_Wavelet:
    def __init__(self, datapath):
        self.datapath = datapath

    def EVIload(self, filename):
        filepath = filename
        image = gdal.Open(filepath, GA_ReadOnly)
        #band = image.GetRasterBand(1)
        cols = image.RasterXSize
        rows = image.RasterYSize
        array = image.ReadAsArray().reshape(cols * rows)
        return array

    def MergeArray(self, idnames):
        merge = numpy.vstack([self.EVIload(filename) for filename in idnames])
        return merge

    def denoise(self, data, wavelet):
        noiseSigma = median(absolute(data - median(data))) / 0.6745
        levels = int(floor(log(len(data))))
        WC = pywt.wavedec(data, wavelet, level=levels)
        threshold = noiseSigma * sqrt(2 * log(len(data)))
        NWC = map(lambda x: pywt.thresholding.hard(x, threshold), WC)
        return pywt.waverec(NWC, wavelet)

    def evi_reshape(self, evi):
        revi = numpy.arange(365, dtype=numpy.float32)
        revi[range(len(revi))] = numpy.nan
        n = 0
        for i in range(len(evi)):
            revi[n] = evi(n)
            n = i * 8
        return revi

    def Interpolate(self, evi):
        t = numpy.array([(i * 8) + 1 for i in range(len(evi))], dtype='float32')
        if evi[0] == -28672.:
            evi[0] = evi[evi != -28672.][0]
        if evi[-1] == -28672.:
            evi[-1] = evi[evi != -28672.][-1]
        evi[evi == -28672.] = numpy.nan
        devi = numpy.delete(evi, numpy.where(numpy.isnan(evi)), 0)
        t = numpy.delete(t, numpy.where(numpy.isnan(evi)), 0)
        #f = interp1d(t, evi)
        rp = splrep(t, devi, s=0)
        ts = numpy.array([i + 1 for i in range(361)],
                         dtype=numpy.float32)
        #evinew = f(ts)
        evinew = splev(ts, rp, der=0)
        return evinew

    def graph(self, listA, listB):
        import matplotlib.pyplot as plt
        plt.ylim(-0.1,0.8)
        plt.plot(listA[0], listA[1], '-r', label="MODIS EVI")
        plt.plot(listB[0], listB[1], '-b', label="Wavelet EVI")
        plt.xticks(rotation=30)
        title = "MODIS EVI in 2005"
        plt.suptitle(title, size='20')
        plt.legend(loc='upper left', fontsize=10)
        plt.show()
