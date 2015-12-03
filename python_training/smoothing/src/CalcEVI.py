# coding: utf-8 -*-
# 2014.08.14 K. Kuwata
# CalcEVI.py
"""
    LandsatやMODIS画像を読み込み、EVIやNDVIを計算
"""

from osgeo import gdal, osr
import numpy


class CalcVI_MODIS:
    def __init__(self, blue_path, red_path, nir_path):
        self.blue = gdal.Open(blue_path,gdal.GA_ReadOnly)
        self.red = gdal.Open(red_path, gdal.GA_ReadOnly)
        self.nir = gdal.Open(nir_path, gdal.GA_ReadOnly)
        self.geo = self.blue.GetGeoTransform()
        self.projection = self.blue.GetProjection()
        self.cols = self.blue.RasterXSize
        self.rows = self.blue.RasterYSize
        self.nil = -28672.

    def Reflectance(self, band):
        Array = band.ReadAsArray().reshape(self.cols * self.rows)
        Array = numpy.where(Array.astype(numpy.float32) != self.nil,
                            Array.astype(numpy.float32) * 0.0001,
                            self.nil)
        return Array

    def CalcNDVI(self):
        Red = self.Reflectance(self.red)
        Nir = self.Reflectance(self.nir)
        denominator = numpy.where(Nir != self.nil,
                                  Nir + Red,
                                  self.nil)
        numerator = numpy.where(Nir != self.nil,
                                Nir - Red,
                                self.nil)
        NDVI = numpy.where((denominator != 0.) & (denominator != self.nil),
                           numerator / denominator,
                           self.nil)
        del Red, Nir, denominator, numerator
        return NDVI

    def CalcEVI(self):
        Blue = self.Reflectance(self.blue)
        Red = self.Reflectance(self.red)
        Nir = self.Reflectance(self.nir)
        G = 2.5
        L = 1.
        C1 = 6.
        C2 = 7.5
        denominator = numpy.where((Nir != self.nil) & (Red != self.nil) & (Blue != self.nil) & (Blue <= 1.0),
                                  Nir + (C1*Red) - (C2*Blue) + L,
                                  self.nil)
        numerator = numpy.where((Nir != self.nil) & (Red != self.nil),
                                (Nir - Red) * G,
                                self.nil)
        EVI = numpy.where((denominator != 0.) & (denominator != self.nil),
                          numerator / denominator,
                          self.nil)
        del Blue, Red, Nir, G, L, C1, C2, denominator, numerator
        return numpy.where(EVI > 0., EVI, self.nil)

    def EVI_TIFF(self, path):
        EVI = self.CalcEVI()
        originX = self.geo[0]
        originY = self.geo[3]
        pixelWidth = self.geo[1]
        pixelHeight = self.geo[5]
        Array = EVI.reshape([self.rows, self.cols])
        driver = gdal.GetDriverByName('GTiff')
        outRaster = driver.Create(path, self.cols, self.rows, 1, gdal.GDT_Float32)
        outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(Array)
        outRasterSRS = osr.SpatialReference()
        outRasterSRS.ImportFromEPSG(4326)
        outRaster.SetProjection(outRasterSRS.ExportToWkt())
        outband.FlushCache()


