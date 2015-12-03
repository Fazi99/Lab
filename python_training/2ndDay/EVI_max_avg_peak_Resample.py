# -*- coding: utf-8 -*-
# 2015.04.04 K. Kuwata
# 2015.07.04 Faizan
# EVI_standardize.py
__author__ = 'ken'

from lib.GdalHandle import GImage
from lib.GdalHandle import MultiImages
import os
import numpy
from osgeo import gdal, osr

path="/home/faizan/HDD1/EVI/resample"
name="/Pak_crop"
def resample1(array):
    r_array = array.copy()
    r_array[:] = 0
    rows = array.shape[0]
    cols = array.shape[1]
    for y in range(0, rows):
        for x in range(0, cols):
            if array[y,x] > -9999:
                if array[y,x] != 0:
                    r_array[y, x] = 1
    return r_array

def find_max_evi_date(mask, year, start, end):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(start, end) ]
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        results[i] = numpy.where(array == array.max())[0][0] + (start-1)
        #results[i] = array.max()
    del AllArrays
    return results

def find_max_evi_value(mask, year, start, end):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(start, end) ]
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        #results[i] = numpy.where(array == array.max())[0][0] + (start-1)
        results[i] = array.max()
    del AllArrays
    return results

def find_avg_evi(year, start, end):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(start, end) ]
    mimage = MultiImages(files)
    AllArrays = mimage.CalcAverage()
    return AllArrays

def find_avg_evi_K(year):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(91,274) ]
    mimage = MultiImages(files)
    AllArrays = mimage.CalcAverage()
    return AllArrays

def find_avg_evi_R(year1, year2):
    file1 = [path+name+".%d%03d"  % (year1, i) + ".5km.tif" for i in range(274, 363) ]
    file2 = [path+name+".%d%03d"  % (year2, j) + ".5km.tif" for j in range(1, 91) ]
    files = file1+file2
    mimage = MultiImages(files)
    AllArrays = mimage.CalcAverage()
    return AllArrays

def find_max_evi_date_K(mask, year):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(91,274) ]
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        #results[i] = numpy.where(array == array.max())[0][0] + 90
        results[i] = array.max()
    del AllArrays
    return results

def find_max_evi_date_R(mask, year1, year2):
    file1 = [path+name+".%d%03d"  % (year1, i) + ".5km.tif" for i in range(274, 363) ]
    file2 = [path+name+".%d%03d"  % (year2, j) + ".5km.tif" for j in range(1, 91) ]
    files=file1+file2
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        results[i] = array.max()
    del AllArrays
    return results

def find_max_evi_date_K(mask, year):
    files = [path+name+".%d%03d"  % (year, i) + ".5km.tif" for i in range(91,274) ]
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        results[i] = numpy.where(array == array.max())[0][0] + 90
    del AllArrays
    return results

def find_max_evi_date_R(mask, year1, year2):
    file1 = [path+name+".%d%03d"  % (year1, i) + ".5km.tif" for i in range(274, 363) ]
    file2 = [path+name+".%d%03d"  % (year2, j) + ".5km.tif" for j in range(1, 91) ]
    files=file1+file2
    mimage = MultiImages(files)
    AllArrays = mimage.Images2Arrays()
    results = numpy.array([0 for i in AllArrays[0]])
    for i in numpy.where(mask.flatten() == 1)[0]:
        array = AllArrays.T[i]
        ind=numpy.where(array == array.max())[0][0]
        if ind < 90:
            N = 273
        else:
            N = -89
        results[i] = ind + N
    del AllArrays
    return results


path1="/home/faizan/HDD1/EVI/resample/Pak_crop.2002099.5km.tif"
ds = gdal.Open(path1)
array = ds.ReadAsArray()

r_array = resample1(array)
#

# for monthly max and avg EVI values
days=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 363]
mon=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
for year in range(2002, 2015):
    for i in range(len(days)-1):
        start=days[i]
        end= days[i+1]
        max_value = find_max_evi_value(r_array, year, start, end)
        avg_value = find_avg_evi(year, start, end)
        image = GImage(path1)
        m=mon[i]
        image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.%s_max_evi_value.tif" % (year,m), Array=max_value)
        image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.%s_avg_evi_value.tif" % (year,m), Array=avg_value)
        #print m
        #del max_value, avg_value
        del avg_value
    print year
"""
# for seasonal max, mean and
#   R "rabi", K    "Kharif"
years=[]
for y in range(2002,2015):
    years.append(y)
for n in range(len(years)):
    image = GImage(path1)
    max_date = find_max_evi_date_K(r_array, years[n])
    image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.kharif_max_evi_date.tif" % (years[n]), Array=max_date)
    del max_date

    avg_value = find_avg_evi_K(years[n])
    image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.kharif_avg_evi_value.tif" % (years[n]), Array=avg_value)
    del avg_value

    max_date = find_max_evi_date_R(r_array, years[n], years[n+1])
    image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.rabi_max_evi_date.tif" % (years[n]), Array=max_date)
    del max_date

    avg_value = find_avg_evi_R(years[n], years[n+1])
    image.Array2Tiff(out_name="/home/faizan/HDD1/EVI/resample/Pak_crop.%d.rabi_avg_evi_value.tif" % (years[n]), Array=avg_value)
    del avg_value
    print years[n]

#datatypes = ["cld", "dtr", "frs", "pet", "pre", "tmn", "tmp", "tmx", "vap", "wet"]
mon=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#mon=["kharif", "rabi"]
def input_lists(month):
    #return ["tiff/cru.%d.%02d.%s.tif" % (year, month, dtype) for year in xrange(1960, 2014)]
    return [path+name+"."+str(year)+"."+month+"_avg_evi_value.tif"   for year in xrange(2002, 2014) ]
    #return ["tiff/MODIS.EVI.MonthlySum.%d%02d.tif" % (year, month) for year in xrange(2001, 2014)]

def output_lists(month):
    return [path+name+"."+str(year)+"."+month+"_evi_anomaly.tif"   for year in xrange(2002, 2014) ]
    #return ["tiff/cru.%d.%02d.%s.anomaly.tif" % (year, month, dtype) for year in xrange(1960, 2014)]
    #return ["tiff/MODIS.EVI.MonthlyAnom.%d%02d.tif" % (year, month) for year in xrange(2001, 2014)]

def Standard(inputs, outputs):
    mimimage = MultiImages(inputs)
    SArrays = mimimage.CalcStandard()
    for (ofile, array) in zip(outputs, SArrays):
        mimimage.Array2Tiff(ofile, array)
        print ofile
    del SArrays, mimimage

if __name__=="__main__":
    for month in mon:
        inputs = input_lists(month)
        outputs = output_lists(month)
        Standard(inputs, outputs)
"""
