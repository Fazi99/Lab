# -*- coding: utf-8 -*-
# script01.py
# 2014.11.20 K. Kuwata

from image import landsat

name= "LE70240322008153EDC00"
# Calculating reflectance of Band1
limage = landsat("/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_B1.TIF", "/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_MTL.txt", 7, 1)

 # Get pixel data as array
array = limage.Band2Array()

 # Get information from a parameter file
Parameters = limage.ReturnParameters()
 # Calculate Radiance from DN
Radiance = limage.DN2Radiance(array, Parameters)
 # Calculate Reflectance from Radiance
Reflectance1 = limage.Radiance2Reflectance(Radiance, Parameters)
 # Make a Geotiff file
limage.WriteArrayAsImage("4_Reflectance_B1_B3.tif", Reflectance1)


# Calculating reflectance of Band3
limage = landsat("/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_B3.TIF", "/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_MTL.txt", 7, 3)

 # Get pixel data as array
array = limage.Band2Array()

 # Get information from a parameter file
Parameters = limage.ReturnParameters()
 # Calculate Radiance from DN
Radiance = limage.DN2Radiance(array, Parameters)
 # Calculate Reflectance from Radiance
Reflectance3 = limage.Radiance2Reflectance(Radiance, Parameters)
 # Make a Geotiff file
limage.WriteArrayAsImage("4_Reflectance_B3_B1.tif", Reflectance3)

# Calculating reflectance of Band4
limage = landsat("/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_B4.TIF", "/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_MTL.txt", 7, 4)

 # Get pixel data as array
array = limage.Band2Array()

 # Get information from a parameter file
Parameters = limage.ReturnParameters()
 # Calculate Radiance from DN
Radiance = limage.DN2Radiance(array, Parameters)
 # Calculate Reflectance from Radiance
Reflectance4 = limage.Radiance2Reflectance(Radiance, Parameters)
 # Make a Geotiff file
limage.WriteArrayAsImage("4_Reflectance_B4_B2.tif", Reflectance4)

# Calculating reflectance of Band5
limage = landsat("/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_B5.TIF", "/home/faizan/USA_data/landsat/4/LE70240322008153EDC00_MTL.txt", 7, 5)

 # Get pixel data as array
array = limage.Band2Array()

 # Get information from a parameter file
Parameters = limage.ReturnParameters()
 # Calculate Radiance from DN
Radiance = limage.DN2Radiance(array, Parameters)
 # Calculate Reflectance from Radiance
Reflectance5 = limage.Radiance2Reflectance(Radiance, Parameters)
 # Make a Geotiff file
limage.WriteArrayAsImage("4_Reflectance_B5_B6.tif", Reflectance5)

# Calculating NDVI
 # Get a pixel column number
#cols = limage.iminfo['cols']
 # Get pixel row number
#rows = limage.iminfo['rows']

 # Calculate NDVI
#NDVI = limage.CalcNDVI(Reflectance4, Reflectance3)

 # Make a Geotiff file
#limage.WriteArrayAsImage("NDVI1landsat.tif", NDVI)
