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
def EVI():
    for y in xrange(2000, 2011):
        lists = [[tifpath + "A%d%03d.US.evi.tif" % (y, m) for m in xrange(001, 362, 8)]]
        array = np.array(lists)
        images = array.reshape(array.shape[0] * array.shape[1])
        n = 0
        array = []
        for j in images:
            if os.path.exists(j) is True:
                image = GImage(j)
                EVI = image.Band2Array(1)
                if n ==0 :
                    EVI = np.where(EVI == fill, 0 , EVI)
                    for k in xrange(len(EVI)):
                        array.append(EVI[k])
                else:
                    array = np.where(EVI == fill, add(array,0) , add(array, EVI))
                n += 1
        print n
        #tif_opath1= tifpath+str(y)+".totalevi.tif"
        #image.WriteArrayAsImage(tif_opath1, array)
        array = array/n
        tif_opath= tifpath+str(y)+".US.evi.tif"
        image.WriteArrayAsImage(tif_opath, array)
        print y
EVI()

