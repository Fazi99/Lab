# -*- coding: utf-8 -*-
# 2015.04.29 Faizan
# annualEVI.py


__author__ = 'Fazi'

from osgeo import ogr
from glob import glob
import  os
import pandas as pd
from numpy.core.umath import add, subtract
import numpy as np

from lib.GdalHandlemulti import GImage

#from lib.projectmanage import Manage
path="/home/faizan/USA_data/8days/pakistan8days/"



#with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:

#manage = Manage("smoothing")

tifpath = "/home/faizan/USA_data/h11v05/"


fill = -999
def Flood():
    for y in xrange(2000, 2015):
        lists = [[path + "A%d%03d.flood.tif" % (y, m) for m in xrange(001, 362, 8)]]
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
        array = array*8
        tif_opath= path+str(y)+".flood.tif"
        image.WriteArrayAsImage(tif_opath, array)
        print y
Flood()

