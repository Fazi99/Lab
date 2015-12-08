# -*- coding: utf-8 -*-
# 2015.15.12 K. Kuwata
# multi.py
__author__ = 'ken'


#from src.lib.MODIS_EVI_Wavelet import MOD_Wavelet
from MODIS_EVI_Wavelet import MOD_Wavelet
from lib.projectmanage import Manage
import glob, numpy, sys, math, os
import pywt
from osgeo import gdal

cdir = os.getcwd()

HOME = os.environ['HOME']

DATA = "MODIS"
product = ""
fill = -999

DATA_path = HOME + "/" + "Data/" + DATA + "/tif"

manage = Manage("wavelet-python")
projectpath = manage.GetProjectPath()
datapath = manage.Datapath(DATA)
wavelet = pywt.Wavelet(pywt.wavelist()[16])

EVI_dir = HOME  + "/Data/" + DATA + "/LSWI/"
numpy_dir = HOME + "/Data/" + DATA + "/numpy/"

modis = MOD_Wavelet(EVI_dir, fill)

def argwrapper(args):
    '''
    ラッパー関数
    '''
    return args[0](*args[1:])

def myfunc(i):
    '''
    並列に計算したい関数
    '''
    evi = numpy.array([merge[j][i] for j in range(n)])
    flag = evi != fill
    if sum(flag) > 20:
        evinew = modis.Interpolate(evi)
        avidenoise = modis.denoise(evinew, wavelet)
        bvidenoise = numpy.array(map(math.floor, avidenoise*10000))
        evidenoise = bvidenoise.astype(numpy.int32)
        del evinew, avidenoise, bvidenoise
    else:
        evidenoise = numpy.array([fill for k in range(362)], dtype=numpy.int32)
    sys.stdout.write("%d \r" % (i))
    sys.stdout.flush()
    del evi, flag
    return evidenoise

def process(merge):
    from multiprocessing import Pool
    p = Pool(10)
    for k in xrange(0, 8):
        func_args = []
        for i in xrange(cols*rows*k/8, cols*rows*(k+1)/8):
            func_args.append((myfunc, i))
        results = numpy.array(p.map(argwrapper, func_args), dtype=numpy.int32)
        del func_args
        numpy.save(numpy_dir + 'evidenoise%d' % (k), results)
        print "evidenoise %d" % (k)
        del results
    del merge
    arrays_path = sorted(glob.glob(numpy_dir + "evidenoise*.npy"))
    array_path = arrays_path[0]
    Array = numpy.load(array_path)
    for array_path in arrays_path[1:]:
        array = numpy.load(array_path)
        Array = numpy.vstack([Array, array])
    t_Array = Array.T
    N = len(t_Array)
    for i in range(N):
        filename = "MODIS.LSWI.%s%03d" % (y, i+1)
        numpy.save(numpy_dir + filename, t_Array[i])
    del t_Array, Array

if __name__ == '__main__':
    #for y in range(2002, 2003):
        y = int(sys.argv[1])
        print y
        inputfiles = sorted(glob.glob(EVI_dir + "MOD09A1.A" + str(y) + "*.LSWI.tif"))
        print inputfiles
        merge = modis.MergeArray(inputfiles)
        numpy.save(numpy_dir + "merge." + str(y), merge)
        print merge.shape
        image = gdal.Open(inputfiles[0], gdal.GA_ReadOnly)
        cols = image.RasterXSize
        rows = image.RasterYSize
        n = len(merge)
        print "%d %d %d" % (cols, rows, n)
        process(merge)
        del merge
