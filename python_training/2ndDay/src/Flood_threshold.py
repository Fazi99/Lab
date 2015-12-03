from index_class import Index


fill=-999

#change file paths accordingly

import numpy
import time
from osgeo import gdal
from numpy.core.umath import add, subtract
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

    def CalcDVEL(self, EVI, LSWI, fill):

        DVEL=numpy.where(LSWI == fill, fill , subtract(EVI,LSWI))
        return DVEL

    def CalcFlood(self, EVI, LSWI, DVEL, fill):
        EVI_1 = numpy.where(EVI<=0.3, 1,0)
        DVEL_1 = numpy.where(DVEL<=0.05,1,0)
        combine =EVI_1+DVEL_1
        check1 = numpy.where(combine==2, 1,0)
        EVI_2 = numpy.where(EVI<=0.05, 1,0)
        LSWI_2 = numpy.where(LSWI<=0.0999,1,0)
        combine=EVI_2+LSWI_2
        check2 = numpy.where(combine==2, 1,0)
        combine = check1 + check2
        flood = numpy.where(combine==2, 1, combine)
        flood = numpy.where(EVI==fill, 255, flood)
        return flood


fill=0

#change file paths accordingly


path_evi="/home/faizan/Pakistan/EVI/"
path_lswi="/home/faizan/HDD1/LSWI/"
path_flood="/home/faizan/HDD1/FLOOD_thresh/"
for year in range(2004,2010):
    n=0
    for i in range(1, 363):

        #assigning names test data
        evi=path_evi+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        lswi=path_lswi+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        Oflood =path_flood+str(year)+"/flood_thr.%d%03d"  % (year, i) + ".tif"

    #Test data
        if os.path.exists(evi) is True:

            limage = Index(evi)
            cols = limage.iminfo['cols']
            rows = limage.iminfo['rows']
            bandnum= limage.iminfo['bandnum']
            EVI = (limage.index2Array())
            limage = Index(lswi)
            LSWI = (limage.index2Array())
            DVEL = limage.CalcDVEL(EVI, LSWI, fill)

            #calculate Flood
            Flood= (limage.CalcFlood(EVI, LSWI, DVEL, fill))
            #Get Flood as tiff
            limage.WriteArrayAsImage(Oflood, Flood)
        print n
        n +=1
        del EVI, LSWI, DVEL, Flood







