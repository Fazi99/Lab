# -*- coding: utf-8 -*-
# 2015.04.04 K. Kuwata
# 2015.07.04 Faizan
# EVI_standardize.py
__author__ = 'ken'

from lib.GdalHandle import GImage
from lib.GdalHandle import MultiImages
import os

datatypes = ["cld", "dtr", "frs", "pet", "pre", "tmn", "tmp", "tmx", "vap", "wet"]

def input_lists(dtype, month):
    return ["tiff/cru.%d.%02d.%s.tif" % (year, month, dtype) for year in xrange(1960, 2014)]
    #return ["tiff/MODIS.EVI.MonthlySum.%d%02d.tif" % (year, month) for year in xrange(2001, 2014)]

def output_lists(dtype, month):
    return ["tiff/cru.%d.%02d.%s.anomaly.tif" % \
            (year, month, dtype) for year in xrange(1960, 2014)]
    #return ["tiff/MODIS.EVI.MonthlyAnom.%d%02d.tif" % (year, month) for year in xrange(2001, 2014)]

def Standard(inputs, outputs):
    mimimage = MultiImages(inputs)
    SArrays = mimimage.CalcStandard()
    for (ofile, array) in zip(outputs, SArrays):
        mimimage.Array2Tiff(ofile, array)
        print ofile
    del SArrays, mimimage

if __name__=="__main__":
    for datatype in datatypes:
        for month in xrange(1, 13):
            inputs = input_lists(datatype, month)
            outputs = output_lists(datatype, month)
            Standard(inputs, outputs)
