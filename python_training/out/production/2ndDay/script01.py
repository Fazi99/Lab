# -*- coding: utf-8 -*-
# script01.py
# 2014.11.20 K. Kuwata

from image import landsat


# Band1
limage = landsat("/Users/ken/Data/Landsat/LE71070352000329EDC00_B3.TIF", "/Users/ken/Data/Landsat/LE71070352000329EDC00_MTL.txt", 7, 3)

array = limage.Band2Array()

Parameters = limage.ReturnParameters()

Radiance = limage.DN2Radiance(array, Parameters)

Reflectance3 = limage.Radiance2Reflectance(Radiance, Parameters)

limage.WriteArrayAsImage("Reflectance_B1.tif", Reflectance3)

# Band3
limage = landsat("/Users/ken/Data/Landsat/LE71070352000329EDC00_B4.TIF", "/Users/ken/Data/Landsat/LE71070352000329EDC00_MTL.txt", 7, 4)

array = limage.Band2Array()

Parameters = limage.ReturnParameters()

Radiance = limage.DN2Radiance(array, Parameters)

Reflectance4 = limage.Radiance2Reflectance(Radiance, Parameters)

cols = limage.iminfo['cols']
rows = limage.iminfo['rows']

NDVI = limage.CalcNDVI(NIR=Reflectance4.reshape(cols * rows), Red=Reflectance3.reshape(cols * rows))

limage.WriteArrayAsImage("NDVI.tif", NDVI.reshape(rows, cols))
