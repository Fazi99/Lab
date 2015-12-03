# -*- coding: utf-8 -*-
# 2015.06.30 Faizan
# SVM flooding


from osgeo import gdal
from sklearn import svm
import numpy
import time
from osgeo import gdal
from sklearn.externals import joblib
from numpy.core.umath import add, subtract
import gc
from multiprocessing import Pool
import os

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

    def index2Array(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows)
        array = array/10000
        array = array.reshape(cols * rows)
        return array

    def index2Array1(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows)
        #array = array/10000
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

#change file paths accordingly


path_evi="/home/faizan/Pakistan/EVI/"
path_lswi="/home/faizan/HDD1/LSWI/"
path_flood="/home/faizan/HDD1/FLOOD/"
np_dir="/home/faizan/Desktop/numpy_dir/"
model='/home/faizan/Desktop/model/modis_trained.pkl'
for year in range(2010,2011):
    for i in range(112, 150):

        #assigning names test data
        evi=path_evi+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        lswi=path_lswi+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        Oflood =path_flood+str(year)+"/flood.%d%03d"  % (year, i) + ".tif"

    #Test data
        if os.path.exists(evi) is True:

            limage = Index(evi)
            cols = limage.iminfo['cols']
            rows = limage.iminfo['rows']
            bandnum= limage.iminfo['bandnum']
            EVI = (limage.index2Array())
            limage = Index(lswi)
            LSWI = (limage.index2Array())
            Data = numpy.vstack([EVI, LSWI])
            del EVI, LSWI

# change the file path
            clf = joblib.load(model)

            def argwrapper(args):
                '''
                ラッパー関数
                '''
                return args[0](*args[1:])

            def myfunc(x):
                '''
                並列に計算したい関数
                '''
                return clf.predict([Data[0][x], Data[1][x], subtract(Data[0][x], Data[1][x])])

        #Process
            start_time = time.time()
            if __name__ == '__main__':
                p = Pool(7)
                for a in xrange(0, 10):
                    func_args = []
                    for i in xrange((len(Data[0])*a)/10, (len(Data[0])*(a+1))/10):
                        func_args.append((myfunc, i))
                    results = numpy.array(p.map(argwrapper, func_args), dtype=numpy.int16)
                    del func_args
                    numpy.save(np_dir + "svm_result%02d" % a, results)
                    del results
                    print("--- %s seconds ---" % (time.time() - start_time))
                del Data
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
