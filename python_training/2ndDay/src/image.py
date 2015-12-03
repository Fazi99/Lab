# -*- coding: utf-8 -*-
# script01.py
# 2014.11.20 K. Kuwata

__author__ = 'ken'

from osgeo import gdal
import numpy
from numpy.core.umath import add, subtract
import datetime
import math

class DSImage(object):
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

class landsat(DSImage):
    def __init__(self, filepath, parafpath, landsatnum, bandnum):
        self.filepath = filepath
        self.parafpath = parafpath
        self.landsatnum = landsatnum
        self.bandnum = bandnum
        super(landsat, self).__init__(filepath)

    def Band2Array(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        array = band.ReadAsArray(0, 0, cols, rows) #.reshape(cols * rows)
        return array

    def MLTFileLoad(self):
        filepath = self.parafpath
        f = open(filepath, 'rb')
        dataReader = f.readlines()
        return dataReader

    def ReturnParameters(self):
        dataReader = self.MLTFileLoad()
        Parameters = {}
        LMIN = "RADIANCE_MINIMUM_BAND_" + str(self.bandnum)
        LMAX = "RADIANCE_MAXIMUM_BAND_" + str(self.bandnum)
        QCAL_MAX = "QUANTIZE_CAL_MAX_BAND_" + str(self.bandnum)
        QCAL_MIN = "QUANTIZE_CAL_MIN_BAND_" + str(self.bandnum)
        SUN_AZI = "SUN_AZIMUTH"
        SUN_ELE = "SUN_ELEVATION"
        DATE = "DATE_ACQUIRED"
        SUN_DIS = "EARTH_SUN_DISTANCE"
        for line in dataReader:
            name = line.split('=')[0].strip()
            if(name == LMIN):
                Parameters[LMIN] = float(line.split('=')[1].strip())
            elif(name == LMAX):
                Parameters[LMAX] = float(line.split('=')[1].strip())
            elif(name == QCAL_MAX):
                Parameters[QCAL_MAX] = float(line.split('=')[1].strip())
            elif(name == QCAL_MIN):
                Parameters[QCAL_MIN] = float(line.split('=')[1].strip())
            elif(name == SUN_AZI):
                Parameters[SUN_AZI] = float(line.split('=')[1].strip())
            elif(name == SUN_ELE):
                Parameters[SUN_ELE] = float(line.split('=')[1].strip())
            elif(name == DATE):
                date = line.split('=')[1].strip()
                Parameters['DOY'] = datetime.datetime.strptime(date, '%Y-%m-%d').timetuple().tm_yday
            elif(name == SUN_DIS):
                Parameters[SUN_DIS] = float(line.split('=')[1].strip())
        if(SUN_DIS in Parameters):
            pass
        else:
            DOY = Parameters['DOY']
            if ( DOY >= 1 and DOY < 15 ): Parameters[SUN_DIS] = 0.9832
            elif ( DOY >= 15 and DOY < 32 ): Parameters[SUN_DIS] = 0.9836
            elif ( DOY >= 32 and DOY < 46 ): Parameters[SUN_DIS] = 0.9853
            elif ( DOY >= 46 and DOY < 60 ): Parameters[SUN_DIS] = 0.9878
            elif ( DOY >= 60 and DOY < 74 ): Parameters[SUN_DIS] = 0.9909
            elif ( DOY >= 74 and DOY < 91 ): Parameters[SUN_DIS] = 0.9945
            elif ( DOY >= 91 and DOY < 106 ): Parameters[SUN_DIS] = 0.9993
            elif ( DOY >= 106 and DOY < 121 ): Parameters[SUN_DIS] = 1.0033
            elif ( DOY >= 121 and DOY < 135 ): Parameters[SUN_DIS] = 1.0076
            elif ( DOY >= 135 and DOY < 152 ): Parameters[SUN_DIS] = 1.0109
            elif ( DOY >= 152 and DOY < 166 ): Parameters[SUN_DIS] = 1.0140
            elif ( DOY >= 166 and DOY < 182 ): Parameters[SUN_DIS] = 1.0158
            elif ( DOY >= 182 and DOY < 196 ): Parameters[SUN_DIS] = 1.0167
            elif ( DOY >= 196 and DOY < 213 ): Parameters[SUN_DIS] = 1.0165
            elif ( DOY >= 213 and DOY < 227 ): Parameters[SUN_DIS] = 1.0149
            elif ( DOY >= 227 and DOY < 242 ): Parameters[SUN_DIS] = 1.0128
            elif ( DOY >= 242 and DOY < 258 ): Parameters[SUN_DIS] = 1.0092
            elif ( DOY >= 258 and DOY < 274 ): Parameters[SUN_DIS] = 1.0057
            elif ( DOY >= 274 and DOY < 288 ): Parameters[SUN_DIS] = 1.0011
            elif ( DOY >= 288 and DOY < 305 ): Parameters[SUN_DIS] = 0.9972
            elif ( DOY >= 305 and DOY < 319 ): Parameters[SUN_DIS] = 0.9925
            elif ( DOY >= 319 and DOY < 335 ): Parameters[SUN_DIS] = 0.9892
            elif ( DOY >= 335 and DOY < 349 ): Parameters[SUN_DIS] = 0.9860
            elif ( DOY >= 349 and DOY < 365 ): Parameters[SUN_DIS] = 0.9843
            elif ( DOY == 365 ): Parameters[SUN_DIS] = 0.9833
        return Parameters

    def ReturnESUN(self):
        if(self.landsatnum == 5):
            if(self.bandnum == 1):
                ESUN = 1969.000
            elif(self.bandnum == 2):
                ESUN = 1840.000
            elif(self.bandnum == 3):
                ESUN = 1551.000
            elif(self.bandnum == 4):
                ESUN = 1044.000
            elif(self.bandnum == 5):
                ESUN = 225.700
            elif(self.bandnum == 6):
                ESUN = 82.07
            elif(self.bandnum == 7):
                ESUN = 1368.000
        elif(self.landsatnum == 7):
            if(self.bandnum == 1):
                ESUN = 1997.000
            elif(self.bandnum == 2):
                ESUN = 1812.000
            elif(self.bandnum == 3):
                ESUN = 1533.000
            elif(self.bandnum == 4):
                ESUN = 1039
            elif(self.bandnum == 5):
                ESUN = 230.8
            elif(self.bandnum == 7):
                ESUN = 84.90
            elif(self.bandnum == 8):
                ESUN = 1362.000
        return ESUN

    def DN2Radiance(self, array, Parameters):
        mask = numpy.greater(array, 0)
        name = "RADIANCE_MINIMUM_BAND_" + str(self.bandnum)
        LMIN = Parameters[name]
        name = "RADIANCE_MAXIMUM_BAND_" + str(self.bandnum)
        LMAX = Parameters[name]
        name = "QUANTIZE_CAL_MIN_BAND_" + str(self.bandnum)
        QCALMIN = Parameters[name]
        name = "QUANTIZE_CAL_MAX_BAND_" + str(self.bandnum)
        QCALMAX = Parameters[name]
        Radiance = ((LMAX - LMIN) / (QCALMAX - QCALMIN) * (array - QCALMIN) + LMIN) * mask
        return Radiance

    def Radiance2Reflectance(self, Radiance, Parameters):
        mask = numpy.greater(Radiance, 0)
        PI = math.pi
        d = Parameters['EARTH_SUN_DISTANCE']
        ESUN = self.ReturnESUN()
        ELE = Parameters['SUN_ELEVATION']
        Solar_Zenith = ( 90.0 - ELE ) * PI / 180.0;
        Reflectance = (PI * Radiance * d * d / ESUN * math.cos(Solar_Zenith)) * mask
        return Reflectance

    def CalcNDVI(self, NIR, Red):
        ndvi_lower = add(NIR, Red)
        ndvi_upper = subtract(NIR, Red)
        NDVI = numpy.where(ndvi_lower == 0, 0.0, ndvi_upper/ndvi_lower)
        return NDVI

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outDS = driver.Create(out_fname, cols, rows, 3, gdal.GDT_Float32)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand
