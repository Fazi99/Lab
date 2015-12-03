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

#from lib.projectmanage import Manage
path="/home/faizan/USA_data/h11v05/"



#with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:

#manage = Manage("smoothing")

tifpath = "/home/faizan/USA_data/h11v05/"

aoipath = "/home/faizan/Desktop/"

poipath = "/home/faizan/USA_data/h11v05/output_far/"

shapeData = ogr.Open(aoipath + "us_far_river.shp")

layer = shapeData.GetLayer()
points = []
for index in xrange(layer.GetFeatureCount()):
    feature = layer.GetFeature(index)
    geometry = feature.GetGeometryRef()
    points.append((geometry.GetX(), geometry.GetY()))

lat = points[0][1]
lon = points[0][0]
"""
def EVI():
    lists = [[tifpath + "A%d%03d.US.evi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2011)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])
    n = 0
    for point in points:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "EVI.far%02d.csv" % (n)
        listData = []
        for j in images:
            if os.path.exists(j) is True:
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = float(image.GetValue(lat, lon))
                listData.append([y, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n
EVI()


def LSWI():
    lists = [[tifpath + "A%d%03d.US.lswi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2011)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])
    n = 0
    for point in points:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "LSWI.far%02d.csv" % (n)
        listData = []
        for j in images:
            if os.path.exists(j) is True:
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = (image.GetValue(lat, lon))
                listData.append([y, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n
LSWI()


def NDVI():
    lists = [[tifpath + "A%d%03d.US.ndvi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2011)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])
    n = 0
    for point in points:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "NDVI.far%02d.csv" % (n)
        listData = []
        for j in images:
            if os.path.exists(j) is True:
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = (image.GetValue(lat, lon))
                listData.append([y, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n
NDVI()
"""
def FLOOD():
    lists = [[tifpath + "A%d%03d.US.flood.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2011)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])
    n = 27
    for point in points[27:63]:
        lat = point[1]
        lon = point[0]
        out_csv = poipath + "FLOOD.far%02d.csv" % (n)
        listData = []
        for j in images:
            if os.path.exists(j) is True:
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = (image.GetValue(lat, lon))
                listData.append([y, value])
        data = pd.DataFrame(listData)
        data.to_csv(out_csv, sep=',', index=False, header=False)
        n += 1
        print n
FLOOD()
