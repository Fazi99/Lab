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
path="/home/faizan/USA_data/8days/pakistan8days/"



#with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:

#manage = Manage("smoothing")

tifpath = "/home/faizan/USA_data/8days/pakistan8days/"

aoipath = "/home/faizan/Desktop/"

poipath = "/home/faizan/USA_data/8days/pakistan8days/output_far/"

shapeData = ogr.Open(aoipath + "pak_jac_point.shp")

layer = shapeData.GetLayer()
points = []
for index in xrange(layer.GetFeatureCount()):
    feature = layer.GetFeature(index)
    geometry = feature.GetGeometryRef()
    points.append((geometry.GetX(), geometry.GetY()))

lat = points[0][1]
lon = points[0][0]

def EVI():
    lists = [[tifpath + "A%d%03d.evi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2015)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])


    for j in images:
        if os.path.exists(j) is True:
            n = 0
            for point in points:
                lat = point[1]
                lon = point[0]
                out_csv = poipath + "EVI.far%02d.csv" % (n)
                listData = []
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = float(image.GetValue(lat, lon))
                listData.append([y, value])
                data = pd.DataFrame(listData)
                data.to_csv(out_csv, sep=',', mode='a', index=False, header=False)
                n += 1
        print j
EVI()


def LSWI():
    lists = [[tifpath + "A%d%03d.lswi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2015)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])

    for j in images:
        if os.path.exists(j) is True:
            n = 0
            for point in points:
                lat = point[1]
                lon = point[0]
                out_csv = poipath + "LSWI.far%02d.csv" % (n)
                listData = []
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = float(image.GetValue(lat, lon))
                listData.append([y, value])
                data = pd.DataFrame(listData)
                data.to_csv(out_csv, sep=',', mode='a', index=False, header=False)
                n += 1
        print j

LSWI()


def NDVI():
    lists = [[tifpath + "A%d%03d.ndvi.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2015)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])

    for j in images:
        if os.path.exists(j) is True:
            n = 0
            for point in points:
                lat = point[1]
                lon = point[0]
                out_csv = poipath + "NDVI.far%02d.csv" % (n)
                listData = []
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = float(image.GetValue(lat, lon))
                listData.append([y, value])
                data = pd.DataFrame(listData)
                data.to_csv(out_csv, sep=',', mode='a', index=False, header=False)
                n += 1
        print j
NDVI()

def FLOOD():
    lists = [[tifpath + "A%d%03d.flood.tif" % (y, m) for m in xrange(001, 362, 8)] for y in xrange(2000, 2015)]
    array = np.array(lists)
    images = array.reshape(array.shape[0] * array.shape[1])

    for j in images:
        if os.path.exists(j) is True:
            n = 0
            for point in points:
                lat = point[1]
                lon = point[0]
                out_csv = poipath + "FLOOD.far%02d.csv" % (n)
                listData = []
                y = os.path.split(j)[1].split(".")[0]
                image = GImage(j)
                value = float(image.GetValue(lat, lon))
                listData.append([y, value])
                data = pd.DataFrame(listData)
                data.to_csv(out_csv, sep=',', mode='a', index=False, header=False)
                n += 1
        print j
FLOOD()
