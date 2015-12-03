# -*- coding: utf-8 -*-
# 2014.09.06 K. Kuwata
# wavelet-evi.py
"""
    EVIをWaveletでノイズ除去及びスムージングし、フェノロジーを推定する
"""

#from src.lib.CalcEVI import CalcVI
from src.lib.MODIS_EVI_Wavelet import MOD_Wavelet
from src.lib.projectmanage import Manage
import glob
import numpy
from datetime import datetime as dt
from datetime import timedelta
from scipy.interpolate import interp1d

DATA = "MODIS"
product = ""
fill = -28672

manage = Manage("wavelet-python")
projectpath = manage.GetProjectPath()
datapath = manage.Datapath(DATA)

#calc = CalcVI(datapath)

#modis = calc.MODIS(datapath, product)

modis = MOD_Wavelet(datapath)

inputfiles = glob.glob(datapath + "/*.EVI.tif")
idnames = [filepath.split("/")[-1].rsplit('.', 2)[0] for filepath in inputfiles]
inputfiles.sort()
merge = modis.MergeArray(idnames)

n = len(merge)
evi = numpy.array([merge[i][0] for i in range(n)])
print evi
start = dt.strptime('20050101', '%Y%m%d')

#t = numpy.array([(i * 8) + 1 for i in range(len(evi))], dtype='float32')
#listA = [t, evi]

evinew = modis.Interpolate(evi)
print evinew
#ts = numpy.array([i + 1 for i in range(362)], dtype='float32')
ts = numpy.array([start + timedelta(i) for i in range(len(evinew))])
ts = ts[evinew != numpy.nan]
evinew = evinew[evinew != numpy.nan]
listA = [ts, evinew]

del merge

import pywt
wavelet = pywt.Wavelet(pywt.wavelist()[16])
evidenoise = modis.denoise(evinew, wavelet)
ts = numpy.array([ start + timedelta(i) for i in range(len(evidenoise))])

#ts = numpy.array([i + 1 for i in range(len(evidenoise))], dtype='float32')

#evidenoise = modis.denoise(evi, wavelet)
#ts = numpy.array([(i * 8) + 1 for i in range(len(evidenoise))], dtype='float32')

listB = [ts, evidenoise]
modis.graph(listA, listB)