# -*- coding: utf-8 -*-
# 2015.04.29 Faizan
# annualEVI.py


__author__ = 'Fazi'

from osgeo import ogr
from glob import glob
import os
import pandas as pd
from numpy.core.umath import add, subtract
import numpy as np

from lib.GdalHandlemulti import GImage

#from lib.projectmanage import Manage
path="/home/faizan/HDD1/FLOOD_thresh/"



#with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:

#manage = Manage("smoothing")

tifpath = "/home/faizan/HDD1/FLOOD_thresh/"


fill = 255
def Flood():
    for y in xrange(2002, 2005):
        lists = [[path+str(y) + "/flood_thr.%d%03d.tif" % (y, m) for m in xrange(91, 335)]]
        array = np.array(lists)
        images = array.reshape(array.shape[0] * array.shape[1])
        n = 0
        array = []
        for j in images:
            if os.path.exists(j) is True:
                image = GImage(j)
                flood = image.Band2Array(1)
                if n ==0 :
                    flood = np.where(flood == fill, 0 , flood)
                    for k in xrange(len(flood)):
                        array.append(flood[k])
                else:
                    array = np.where(flood == fill, add(array,0) , add(array, flood))
                n += 1
        print n
        #tif_opath1= tifpath+str(y)+".totalevi.tif"
        #image.WriteArrayAsImage(tif_opath1, array)
        #array = array*8
        tif_opath= path+str(y)+".flood_K_dur.tif"
        image.WriteArrayAsImage(tif_opath, array)
        print y
Flood()

