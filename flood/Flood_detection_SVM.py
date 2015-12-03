# -*- coding: utf-8 -*-
# 2015.04.29 Faizan
# SVM


__author__ = 'Fazi'

from osgeo import gdal
from sklearn import svm
import numpy
import time
from osgeo import gdal
from sklearn.externals import joblib
from numpy.core.umath import subtract
import gc
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

    def index2Array(self,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows)
        array = array.reshape(cols * rows)
        return array

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outArray= outArray.reshape([rows,cols])
        outDS = driver.Create(out_fname, cols, rows, 1, gdal.GDT_Int16)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand



fill=-999
"""
#path="/home/faizan/USA_data/h10v0/"
#np_dir="/home/faizan/Desktop/numpy_dir/"
#with open('/home/faizan/USA_data/h10v0/list9.txt',"r") as f:
    for line in f:
        l= line.split(".")

        #assigning names test data
        evi=path+str(l[0])+"."+str(l[1])+".US.evi.tif"
        lswi=path+str(l[0])+"."+str(l[1])+".US.lswi.tif"
        Oflood = path+str(l[0])+"."+str(l[1])+".svm.flood.tif"
"""

path="/home/faizan/USA_data/8days/pak_data/"
np_dir="/home/faizan/Desktop/numpy_dir/"
with open('/home/faizan/USA_data/8days/pak_data/list9.txt',"r") as f:
    for line in f:
        l= line.split(".")
        start_time = time.time()
        #assigning names test data
        evi=path+str(l[0])+"."+str(l[1])+".evi.tif"
        lswi=path+str(l[0])+"."+str(l[1])+".lswi.tif"
        Oflood = path+str(l[0])+"."+str(l[1])+".svm.flood.tif"

    #Test data
        limage = Index(evi)
        cols = limage.iminfo['cols']
        rows = limage.iminfo['rows']
        bandnum= limage.iminfo['bandnum']
        EVI = (limage.index2Array(fill))
    #Test data
        limage = Index(lswi)
        LSWI = (limage.index2Array(fill))

        Data = numpy.vstack([EVI, LSWI])
        del EVI, LSWI

        clf = joblib.load('/home/faizan/Desktop/model/modis_trained.pkl')

        def argwrapper(args):
            return args[0](*args[1:])

        def myfunc(x):
            return clf.predict([Data[0][x], Data[1][x], subtract(Data[0][x], Data[1][x])])

    #Process

        if __name__ == '__main__':
            p = Pool(6)

            for a in xrange(0, 10):
                func_args = []
                for i in xrange((len(Data[0])*a)/10, (len(Data[0])*(a+1))/10):
                    func_args.append((myfunc, i))
                results = numpy.array(p.map(argwrapper, func_args), dtype=numpy.int16)
                del func_args
                numpy.save(np_dir + "svm_result%02d" % a, results)
                del results
                print("--- %s seconds ---" % (time.time() - start_time))
            del Data, clf
            p.close()
    # Load all array and merge
            # load first array
            ARRAY = numpy.load(np_dir + "svm_result00.npy")

            for a in range(1, 10):
                dummy = numpy.load(np_dir + "svm_result%02d.npy" % (a))
                ARRAY = numpy.vstack([ARRAY, dummy])
    # Write image
            limage.WriteArrayAsImage(Oflood, ARRAY)
            del ARRAY, dummy
            gc.collect()

f.close()