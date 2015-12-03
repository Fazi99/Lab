# -*- coding: utf-8 -*-
# 2015.03.06 K. Kuwata
# GetValue.py
"""
    画像から値を取得する
"""

__author__ = 'ken'

from osgeo import ogr
from glob import glob
import csv, os
import pandas as pd
import numpy as np

from lib.GdalHandlemulti import GImage
from lib.projectmanage import Manage

manage = Manage("smoothing")

tifpath = manage.projectpath + "/tiff/"

aoipath = manage.projectpath + "/AOI/"

poipath = manage.projectpath + "/POI/"

shapeData = ogr.Open(aoipath + "deeplearning.shp")

layer = shapeData.GetLayer()
points = []
for index in xrange(layer.GetFeatureCount()):
    feature = layer.GetFeature(index)
    geometry = feature.GetGeometryRef()
    points.append((geometry.GetX(), geometry.GetY()))

lat = points[0][1]
lon = points[0][0]

def CropIndex():
    #images = sorted(glob("/Users/ken/workspace/Research/cornyield_est/PythonHandle/output/AnnualYield/*AnnualYield.tif"))
    images = ["/Users/ken/workspace/Research/cornyield_est/PythonHandle/output/AnnualYield/%d.AnnualYield.tif" % (year) for year in range(2001, 2011)]
    n = 0
    for point in points:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "CropIndex%02d.csv" % (n)
        listData = []
        for j in images:
            y = os.path.split(j)[1].split(".")[0]
            image = GImage(j)
            value = image.GetValue(lat, lon)
            listData.append([y, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n

CropIndex()

def Climate():
    types = ["2t", "dpd", "ssr", "tp"]
    for t in types:
        #images = sorted(glob("/Users/ken/workspace/Research/cornyield_est/PythonHandle/output/Clip/" + t + "*MonthlySum.Clip.tif"))
        path = "/Users/ken/workspace/Research/cornyield_est/PythonHandle/output/Clip/"
        images = []
        for year in range(2001, 2011):
            images = images + [path +
                               "%s.%d.%02d.MonthlySum.Clip.tif" % (t, year, month)
                                for month in range(1, 13)]
        print images
        n = 0
        for point in points:
            lat = point[1]
            lon = point[0]
            out_csv = poipath + t + ".MonthlySum%02d.csv" % (n)
            listData = []
            for j in images:
                y = ".".join(os.path.split(j)[1].split(".")[1:3])
                image = GImage(j)
                value = image.GetValue(lat, lon)
                listData.append([y, value])
            data = pd.DataFrame(listData)
            data.to_csv(out_csv, sep=',', index=False, header=False)
            n += 1
            print t, n

Climate()

def EVI():
    lists = [[tifpath + "MODIS.EVI.MonthlySum.%d%02d.tif" % (y, m) for m in xrange(1, 13)] for y in xrange(2001, 2011)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])
    n = 0
    for point in points:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "EVI.MonthlySum%02d.csv" % (n)
        listData = []
        for j in images:
            y = os.path.split(j)[1].split(".")[3][0:4]
            m = os.path.split(j)[1].split(".")[3][-2:]
            image = GImage(j)
            value = image.GetValue(lat, lon)
            listData.append([y + "." + m, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n

#EVI()
