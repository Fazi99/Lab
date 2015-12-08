# -*- coding: utf-8 -*-
# 2014.11.08 K. Kuwata
# GdalHandle.py

"""
    地理空間情報を含んだ画像データを処理・扱う
"""

from osgeo import gdal, osr
import numpy
import subprocess
from subprocess import PIPE, Popen
import os
import math

def quicksort(seq):
    if len(seq) < 1:
        return seq
    pivot = seq[0]
    left = []
    right = []
    for x in range(1, len(seq)):
        if seq[x] <= pivot:
            left.append(seq[x])
        else:
            right.append(seq[x])
    left = quicksort(left)
    right = quicksort(right)
    foo = [pivot]
    return left + foo + right

class DSImage(object):
    def __init__(self, impath):
        self.impath = impath
        self.ds = gdal.Open(self.impath, gdal.GA_ReadOnly)

class GImage(DSImage):
    def __init__(self, impath):
        super(GImage, self).__init__(impath)
        self.iminfo = dict()
        self.iminfo['bandnum'] = self.ds.RasterCount
        self.iminfo['cols'] = self.ds.RasterXSize
        self.iminfo['rows'] = self.ds.RasterYSize
        self.iminfo['originX'] = self.ds.GetGeoTransform()[0]
        self.iminfo['originY'] = self.ds.GetGeoTransform()[3]
        self.iminfo['pixelWidth'] = self.ds.GetGeoTransform()[1]
        self.iminfo['pixelHeight'] = self.ds.GetGeoTransform()[5]

    def Band2Array(self, bn):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(bn)
        array = band.ReadAsArray(0, 0, cols, rows).reshape(cols * rows)
        return array

    def ArrayAllBands(self):
        bandnum = self.iminfo['bandnum']
        AllArrays = numpy.vstack([self.Band2Array(bn+1) for bn in range(bandnum)])
        return AllArrays

    def SumAllArrays(self):
        AllArrays = self.ArrayAllBands()
        SumArray = numpy.array(numpy.sum(AllArrays, axis=0))
        return SumArray

    def Array2Tiff(self, out_name, Array):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        originX = self.iminfo['originX']
        originY = self.iminfo['originY']
        #originX = 0.0
        #originY = 90.0
        pixelWidth = self.iminfo['pixelWidth']
        pixelHeight = self.iminfo['pixelHeight']
        Array = Array.reshape([rows, cols])
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(out_name, cols, rows, 1, gdal.GDT_Float64)
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(Array)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()

    def ResetOriginLocation(self, out_name, GeoTrans):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        pixelWidth = self.iminfo['pixelWidth']
        pixelHeight = self.iminfo['pixelHeight']
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(out_name, cols, rows, 1, gdal.GDT_Float64)
        outRaster.SetGeoTransform(GeoTrans)
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(self.ds.ReadAsArray())
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()

    def FileCheckDel(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    def ResampleWithGdalwarp(self, infile, outfile, newcols, \
                             newrows, method):
        self.FileCheckDel(outfile)
        command = ['gdalwarp', '-ts', str(newcols), str(newrows),\
                   '-r', method, '-of', 'GTiff', infile, outfile]
        command = [comm.encode('utf-8') for comm in command]
        p = subprocess.Popen(command, \
                            stdin=PIPE, \
                            stdout=PIPE, \
                            stderr=PIPE)
        p.wait()

    def ClipWithGdalwarp(self, infile, outfile, shape):
        self.FileCheckDel(outfile)
        layer = os.path.split(os.path.splitext(shape)[0])[1]
        command = ['gdalwarp', '-of', 'GTiff', '-cutline', shape, '-cl',\
                   layer, '-crop_to_cutline', infile, outfile]
        command = [comm.encode('utf-8') for comm in command]
        p = subprocess.Popen(command, \
                            stdin=PIPE, \
                            stdout=PIPE, \
                            stderr=PIPE)
        p.wait()
        #print "stdout: %s" % (p.stdout.readlines(), )
        #print "Erros: %s" % (p.stderr.readlines(), )

    def GetValue(self, lat, lon):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        originX = self.iminfo['originX']
        originY = self.iminfo['originY']
        resX = self.iminfo['pixelWidth']
        resY = self.iminfo['pixelHeight']
        max_x = originX + (cols * abs(resX))
        min_y = originY - (rows * abs(resY))
        if max_x > lon and originX < lon and originY > lat and min_y < lat:
            array = self.ds.ReadAsArray().reshape(cols * rows)
            nx = int((lat - originY) / resY) * cols
            ny = int((lon - originX) / resX)
            N = nx + ny
            return array[N]
        else:
            print "Out of image range!"
            return numpy.nan


    def Array2TiffFromImage(self, out_name, Array):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outDS = driver.Create(out_name, cols, rows, 3, gdal.GDT_Float64)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjectionRef())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(Array)
        outDS = None
        del outDS, outBand


class MultiImages:
    def __init__(self, inputlist):
        self.inputlist = inputlist
        self.ds = gdal.Open(self.inputlist[0], gdal.GA_ReadOnly)
        self.iminfo = dict()
        self.iminfo['bandnum'] = self.ds.RasterCount
        self.iminfo['cols'] = self.ds.RasterXSize
        self.iminfo['rows'] = self.ds.RasterYSize
        self.iminfo['originX'] = self.ds.GetGeoTransform()[0]
        self.iminfo['originY'] = self.ds.GetGeoTransform()[3]
        self.iminfo['pixelWidth'] = self.ds.GetGeoTransform()[1]
        self.iminfo['pixelHeight'] = self.ds.GetGeoTransform()[5]
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        AllArrays = band.ReadAsArray(0, 0, cols, rows).reshape(cols * rows)
        for infile in self.inputlist[1:]:
            im = gdal.Open(infile, gdal.GA_ReadOnly)
            band = im.GetRasterBand(1)
            array = band.ReadAsArray(0, 0, cols, rows).reshape(cols * rows)
            AllArrays = numpy.vstack([AllArrays, array])
        self.AllArrays = AllArrays

    def Images2Arrays(self):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        im = gdal.Open(self.inputlist[0], gdal.GA_ReadOnly)
        band = im.GetRasterBand(1)
        AllArrays = band.ReadAsArray(0, 0, cols, rows).reshape(cols * rows)
        for infile in self.inputlist[1:]:
            im = gdal.Open(infile, gdal.GA_ReadOnly)
            band = im.GetRasterBand(1)
            array = band.ReadAsArray(0, 0, cols, rows).reshape(cols * rows)
            AllArrays = numpy.vstack([AllArrays, array])
        return AllArrays

    def SumAllArrays(self):
        AllArrays = self.AllArrays
        SumArray = numpy.sum(AllArrays, axis=0)
        return SumArray

    def CalcAverage(self):
        AllArrays = self.AllArrays
        SumArray = numpy.sum(AllArrays, axis=0)
        n = AllArrays.shape[0]
        AverageArray = SumArray / n
        return AverageArray

    def CalcSD(self):
        AllArrays = self.AllArrays
        n = AllArrays.shape[0]
        AverageArrays = self.CalcAverage()
        SDArray = numpy.sqrt(numpy.sum((AllArrays - AverageArrays) * (AllArrays - AverageArrays), axis=0) / n)
        return SDArray

    def CalcStandard(self):
        AllArrays = self.AllArrays
        AverageArrays = self.CalcAverage()
        SDArray = self.CalcSD()
        SArrays = (AllArrays - AverageArrays) / SDArray
        return SArrays

    def TransTimeline(self):
        TAllArrays = self.AllArrays.T
        return TAllArrays

    def Array2Tiff(self, out_name, Array):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        originX = self.iminfo['originX']
        originY = self.iminfo['originY']
        #originX = 0.0
        #originY = 90.0
        pixelWidth = self.iminfo['pixelWidth']
        pixelHeight = self.iminfo['pixelHeight']
        Array = Array.reshape([rows, cols])
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(out_name, cols, rows, 1, gdal.GDT_Float64)
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(Array)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()