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

    def Band2Array(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows)
        #array [array <-100] =fill
        #array = numpy.where(array ==fill, fill , array * 0.0001)
        array= array.reshape(cols*rows)
        return  array

    def trtData(self,evi,lswi,dvel):
        X=[]
        for i in range(len(evi)):
            F=[]
            F.append(evi[i])
            F.append(lswi[i])
            F.append(dvel[i])
            #F.append(subtract(evi[i],lswi[i]))
            X.append(F)
        return X

    def trainResult(self, flood):
        y = []
        for i in range(len(flood)):
            y.append(flood[i])
        return y

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
        outDS = driver.Create(out_fname, cols, rows, 1, gdal.GDT_Float32)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand

    def cMatrix(self, actual, test):
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


"""
path="/home/faizan/USA_data/h11v05/"


#assigning names training data

Tevi=path+"evi_t.tif"
Tdvel=path+"dvel_t.tif"
Tlswi=path+"lswi_t.tif"
Tflood=path+"flood_t.tif"

#loading image training
limage = Index(Tevi)
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
bandnum= limage.iminfo['bandnum']
EVI_t = (limage.index2Array(fill))

limage = Index(Tlswi)
LSWI_t = (limage.index2Array(fill))

limage = Index(Tdvel)
DVEL_t = (limage.index2Array(fill))

limage = Index(Tflood)
Flood_t = (limage.index2Array(fill))

# arranging training data
X = (limage.trtData(EVI_t, LSWI_t, DVEL_t))
Y = (limage.trainResult(Flood_t))
# SVM machine learning
clf = svm.SVC()
clf = clf.fit(X,Y)

#save model

joblib.dump(clf, '/home/faizan/Desktop/full/trained.pkl')
"""
clf = joblib.load('/home/faizan/Desktop/full/trained.pkl')
fill=-999

path="/home/faizan/USA_data/h11v05/"
np_dir="/home/faizan/Desktop/numpy_dir/"
with open('/home/faizan/USA_data/h11v05/list99.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split(".")
        #assigning names test data
        evi=path+str(l[0])+".US.evi.tif"
        dvel=path+str(l[0])+".US.dvel.tif"
        lswi=path+str(l[0])+".US.lswi.tif"
        Oflood = path+str(l[0])+".US.mflood.tif"
        #save model

        #joblib.dump(clf, '/home/faizan/Desktop/full/trained.pkl')

        #Test data
        limage = Index(evi)

        cols = limage.iminfo['cols']
        # Get pixel row number
        rows = limage.iminfo['rows']
        bandnum= limage.iminfo['bandnum']
        EVI = (limage.index2Array(fill))

        limage = Index(lswi)
        LSWI = (limage.index2Array(fill))

        limage = Index(dvel)
        DVEL = (limage.index2Array(fill))

        #Data = (limage.trtData(EVI, LSWI, DVEL))
        Data = numpy.vstack([EVI, LSWI, DVEL])
        del EVI, LSWI, DVEL

        def argwrapper(args):
            '''
            ラッパー関数
            '''
            return args[0](*args[1:])

        def myfunc(x):
            '''
            並列に計算したい関数
            '''
            return clf.predict([Data[0][x], Data[1][x], Data[2][x]])

        start_time = time.time()
        if __name__ == '__main__':
            from multiprocessing import Pool
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
            del Data
            # Load all array and merge
            # load first array
            ARRAY = numpy.load(np_dir + "svm_result00.npy")

            for a in range(1, 10):
                dummy = numpy.load(np_dir + "svm_result%02d.npy" % (a))
                ARRAY = numpy.vstack([ARRAY, dummy])
            limage.WriteArrayAsImage(Oflood, ARRAY)
            del ARRAY, dummy
f.close()