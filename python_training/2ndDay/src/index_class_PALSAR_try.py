from osgeo import gdal
import numpy
from numpy.core.umath import add, subtract
from numpy.core.umath import power as po
import cv2
import datetime
import math

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
        #self.factor= factor
        self.fill=fill
        #x1 = band.ReadAsArray()
        x1 = cv2.imread(fill)
        x1 = cv2.cvtColor(x1, cv2.COLOR_BGR2GRAY)
        x1 = cv2.medianBlur(x1,3)

        array = x1.copy()

        array = numpy.array(array, numpy.uint8)
        thresh, array2 = cv2.threshold(array , 0 , 255, cv2.THRESH_BINARY)
        #x1 = cv2.GaussianBlur(x1,(5,5),0)
        #x1 = x1.astype(numpy.float64)
        #x1 = x1.reshape(cols * rows)


        #Arraylog = array.copy()
        #Arraylog[array!=0.] = ((10*numpy.log10(array[array!=0.])) - 83.0)
        #Arraylog = Arraylog.reshape([rows, cols])
        #array = numpy.log10(array)
        #array [array ==0] =fill/home/faizan/USA_data/june2008/A2008161.sur_refl_b01_1.tif
        #array = ((10*numpy.log10(array))-83.0)
        return array2

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outDS = driver.Create(out_fname, cols, rows, 1, gdal.GDT_UInt16)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand

    def CalcFlood(self, BS):
        flood = numpy.where(BS>=-19.01675, 1, 0)
        return flood



