# -*- coding: utf-8 -+-
# 2015.01.16 K. Kuwata
# array2tiff.py
"""
    numpyのarrayをTiffに変換
使い方:
1. インポートする
from array2tiff import na2tiff

2. インスタンスを作成する
tiff = na2tiff("EVI.tif")

    上記の"EVI.tif"とは、切り出したMODISのEVIのTiffファイル。
    画像の位置情報を取得するために選択。
    一度切り出した画像ファイルならなんでも良い。

3. numpyのarrayをTiffファイルに変換
tiff.Array2Tiff("output.tif", array)

    一時期のarrayを一枚の画像へと出力する。
    for文で書く場合、以下のようになる。

tiff = na2tiff("EVI.tif")
for i in range(361):
    outname = "MODIS.2015.%03d.Wavelet.EVI.tif" % (i+1)
    tiff.Array2Tiff(outname, merge_array[i])

    merge_arrayは、Wavelet変換し、転置したarray
"""
__author__ = 'ken'

from osgeo import gdal, osr
import numpy

class na2tiff:
    def __init__(self, ref_image):
        ds = gdal.Open(ref_image, gdal.GA_ReadOnly)
        self.iminfo = dict()
        self.iminfo['cols'] = ds.RasterXSize
        self.iminfo['rows'] = ds.RasterYSize
        self.iminfo['originX'] = ds.GetGeoTransform()[0]
        self.iminfo['originY'] = ds.GetGeoTransform()[3]
        self.iminfo['pixelWidth'] = ds.GetGeoTransform()[1]
        self.iminfo['pixelHeight'] = ds.GetGeoTransform()[5]

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