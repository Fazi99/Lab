from osgeo import gdal
import numpy
from numpy.core.umath import add, subtract
import pandas as pd
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

    def Band2Array(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows)
        #array= array.reshape(cols*rows)
        return array

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outDS = driver.Create(out_fname, cols, rows, 1, gdal.GDT_Int16)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand

    def CalcLCD (self, LCD, fill):
        LCD [LCD == 1] = 4
        LCD [LCD == 2] = 4
        LCD [LCD == 3] = 4
        LCD [LCD == 4] = 4
        LCD [LCD == 5] = 4
        LCD [LCD == 6] = 3
        LCD [LCD == 7] = 3
        LCD [LCD == 8] = 6
        LCD [LCD == 9] = 6
        LCD [LCD == 10] = 3
        LCD [LCD == 11] = 2
        LCD [LCD == 12] = 1
        LCD [LCD == 13] = 5
        LCD [LCD == 14] = 1
        LCD [LCD == 15] = 7
        LCD [LCD == 16] = 6
        LCD [LCD == 0] = 2
        LCD [LCD >= 254] = fill
        return LCD




