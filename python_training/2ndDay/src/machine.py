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

    def Band2Array(self,factor,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        self.fill=fill
        array = band.ReadAsArray(0, 0, cols, rows)
        #array [array <-100] =fill
        #array = numpy.where(array ==fill, fill , array * 0.0001)
        array= array.reshape(cols*rows)
        return  array

    def trtData(self,evi,lswi,dvel):
        self.evi=evi
        self.lswi=lswi
        self.dvel=dvel
        X=[]
        for i in range(len(evi)):
            F=[]
            F.append(evi[i])
            F.append(lswi[i])
            F.append(dvel[i])
            #F.append(subtract(evi[i],lswi[i]))
            X.append(F)
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

    def csv2Array(self,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        path = "/home/faizan/Desktop/full/result.csv"
        data = numpy.genfromtxt(path, dtype=float, delimiter=',')
        array = data.reshape(cols * rows)
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


    def CalcMLSWI ( self , NIR , SWIR, fill):
        mlswi_lower = numpy.where (NIR == fill, fill , add (NIR , SWIR))
        mlswi_upper = numpy.where (NIR == fill, fill ,subtract (NIR , SWIR))
        #Mask = Numpy.Greater (Ndvi_lower, 0)
        mlswi_lower = numpy.where (mlswi_lower == 0 , fill , mlswi_lower)
        lower = (1-mlswi_lower)
        lower = numpy.where (lower == 0 , fill , lower)
        mlswi = numpy.where (mlswi_lower == fill , fill , (1-mlswi_upper)/lower)
        #mlswi1= numpy.where (((mlswi>= 0.75) & (mlswi <= 1.0)), 1, 0)
        #MLSWI = numpy.where (NIR == fill , fill , mlswi1 )

        return mlswi



    def CalcFlood(self, EVI, LSWI, DVEL, fill):
        #mask_evi = EVI <= 0.3
        #mask_dvel = DVEL <= 0.05
        #mask = mask_evi * mask_dvel
        #NDVI[[EVI<=0.3] & [DVEL<=0.05]] = 1
        #NDVI[[EVI<=0.05] and [LSWI<=0.0999]]=1
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
        flood = numpy.where(EVI==fill, fill, flood)
        return flood



