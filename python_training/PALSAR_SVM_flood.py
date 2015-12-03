# -*- coding: utf-8 -*-
# 2015.04.29 Faizan
# SVM


__author__ = 'Fazi'

from osgeo import gdal
import numpy
import time
from numpy.core.umath import add, subtract
import numpy as np
from sklearn import svm
from osgeo import gdal
from sklearn.externals import joblib
from multiprocessing import Pool


class MDimage(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.ds = gdal.Open(filepath, gdal.GA_ReadOnly)
        self.iminfo = dict()
        self.iminfo['bandnum'] = self.ds.RasterCount
        self.iminfo['cols'] = self.ds.RasterXSize
        self.iminfo['rows'] = self.ds.RasterYSize
        self.iminfo['originX'] = self.ds.GetGeoTransform()[0]
        self.iminfo['originY'] = self.ds.GetGeoTransform()[3]
        self.iminfo['pixelWidth'] = self.ds.GetGeoTransform()[1]
        self.iminfo['pixelHeight'] = self.ds.GetGeoTransform()[5]

class Index(MDimage):
    def __init__(self, filepath):
        self.filepath = filepath
        super(Index, self).__init__(filepath)

    def Band2Array(self,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        self.fill=fill
        array = band.ReadAsArray(0, 0, cols, rows)
        array= array.reshape(cols*rows)
        return  array

    def trtData(self,bs):
        self.bs=bs
        X=[]
        for i in range(len(bs)):
            A=[]
            A.append(bs[i])
            X.append(A)
        return X

    def trainResult(self,flood):
        self.flood=flood
        Y=[]
        for i in range(len(flood)):
            Y.append(flood[i])
        return Y

    def index2Array(self,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        self.fill=fill
        array = band.ReadAsArray(0, 0, cols, rows)
        array = array.reshape(cols * rows)
        return  array

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        self.outArray = outArray
        outArray= outArray.reshape([rows,cols])
        outDS = driver.Create(out_fname, cols, rows, 1, gdal.GDT_Float32)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand

    def cMatrix(self, actual, test):
        self.actual=actual
        self.test=test
        F_F=0
        F_N=0
        F_fi=0
        N_F =0
        N_N =0
        N_fi=0
        Fi_F=0
        Fi_N=0
        Fi_fi=0

        for i in range(len(actual)):
            if actual[i]==test[i]:
                if actual[i]==0:
                    N_N += 1
                elif actual[i]==1:
                    F_F += 1
                else:
                    Fi_fi += 1
            else:
                if actual[i]==0:
                    if test[i]==1:
                        N_F += 1
                    else:
                        N_fi+= 1
                elif actual[i]==1:
                    if test[i]==0:
                        F_N +=1
                    else:
                        F_fi +=1
                else:
                    if test[i]==1:
                        Fi_F +=1
                    else:
                        Fi_N +=1

        LIST= [F_F,F_N,F_fi,N_F,N_N,
               N_fi,Fi_F,Fi_N,Fi_fi]

        C_matrix = numpy.array(LIST).reshape(3,3)
        return C_matrix

fill=-999
path="/home/faizan/Desktop/full/"
np_dir="/home/faizan/Desktop/numpy_dir/"
"""
#assigning names training data

bs_t=path+"BS_t_hv.tif"
flood_t=path+"PFlood.tif"

#loading image training
limage = Index(bs_t)
BS_t = (limage.index2Array(fill))

limage = Index(flood_t)
Flood_t = (limage.index2Array(fill))

# arranging training data
X = (limage.trtData(BS_t))
Y = (limage.trainResult(Flood_t))
# SVM machine learning

clf = svm.SVC()
clf = clf.fit(X,Y)

#save model

joblib.dump(clf, '/home/faizan/Desktop/full/Palsar_hv_finaltraining.pkl')
del BS_t, Flood_t, X, Y

"""

#assigning names test data
bs=path+"HH.ALPSRP245160540.backscatter_try.tif"
Oflood = path+"HH.ALPSRP245160540_flood.tif"

#bs=path+"238540.tif"
#Oflood = path+"238540_flood1.tif"
#save model

#joblib.dump(clf, '/home/faizan/Desktop/full/trained.pkl')
clf = joblib.load('/home/faizan/Desktop/full/Palsar_finaltraining.pkl')

#del EVI_t, LSWI_t, DVEL_t, Flood_t, X, Y
#Test data
limage = Index(bs)

cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
bandnum= limage.iminfo['bandnum']
BS = (limage.index2Array(fill))

Data = (limage.trtData(BS))

del BS

def argwrapper(args):
    '''
    ラッパー関数
    '''
    return args[0](*args[1:])

def myfunc(x):
    '''
    並列に計算したい関数
    '''
    return clf.predict(Data[x])
start_time = time.time()

if __name__ == '__main__':
    p = Pool(6)
    for a in xrange(0,40):
        func_args = []
        for i in xrange((len(Data)*a)/40, (len(Data)*(a+1))/40):
            x= i
            func_args.append( (myfunc, x) )
        results = numpy.array(p.map(argwrapper, func_args), dtype=numpy.int16)
        del func_args
        numpy.save(np_dir + "svr_result%02d" % a, results)
        del results
        print("--- %s seconds ---" % (time.time() - start_time))
    del Data
    # Load all array and merge
    # load first array
    ARRAY = numpy.load(np_dir + "svr_result00.npy")

    for a in range(1,40):
        dummy = numpy.load(np_dir + "svr_result%02d.npy" % (a))
        ARRAY = numpy.vstack([ARRAY, dummy])
    limage.WriteArrayAsImage(Oflood, ARRAY)
    del ARRAY, dummy

