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
path="/home/faizan/USA_data/PALSAR/corr/540/"



#with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:

#manage = Manage("smoothing")

tifpath = path

aoipath = "/home/faizan/Desktop/"

poipath = "/home/faizan/USA_data/PALSAR/output/"

shapeData = ogr.Open(aoipath + "Pak_wat_points.shp")

layer = shapeData.GetLayer()
points = []
for index in xrange(layer.GetFeatureCount()):
    feature = layer.GetFeature(index)
    geometry = feature.GetGeometryRef()
    points.append((geometry.GetX(), geometry.GetY()))

lat = points[0][1]
lon = points[0][0]

def BSCT():
    with open(path+'list.txt',"r") as f:
        lists=[]
        for line in f:
            l=line.split("\n")
            print l
            lists = lists+[tifpath + str(l[0])]
        print lists
        images = lists
        print images
        n = 0
        for point in points:
            lat = point[1]
            lon = point[0]
            out_csv = poipath + "540backscatter%02d.csv" % (n)
            listData = []
            for j in images:
                if os.path.exists(j) is True:
                    y = os.path.split(j)[1].split(".")[0]
                    z = os.path.split(j)[1].split(".")[1]
                    image = GImage(j)
                    value = (image.GetValue(lat, lon))
                    listData.append([y,z, value])
            data = pd.DataFrame(listData)
            data.to_csv(out_csv, sep=',', index=False, header=False)
            n += 1
            print n
    f.close()
BSCT()


