# -*- coding: utf-8 -*-
# 2015.04.29 Faizan
# SVM


__author__ = 'Fazi'


from osgeo import gdal, osr
import numpy
import subprocess
from subprocess import PIPE, Popen
import os
import sys
sys.path.append('/usr/bin/')
import gdal_merge as gm
from multiprocessing import Pool
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
        array = band.ReadAsArray(0, 0, cols, rows)
        #array = array.reshape(cols * rows)
        return array

    def FileCheckDel(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

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
        print "stdout: %s" % (p.stdout.readlines(), )
        #print "Erros: %s" % (p.stderr.readlines(), )


    def MergeWithGdalwarp(self, infile, outfile):
        self.FileCheckDel(outfile)
        NO_DATA_VALUE = '-999'

        command = ['gdal_merge.py', '-o', outfile,'-n', NO_DATA_VALUE, '-a_nodata', '255',
         infile[0], infile[1], infile[2], infile[3]]
        command = [comm.encode('utf-8') for comm in command]
        p = subprocess.Popen(command, \
                            stdin=PIPE, \
                            stdout=PIPE, \
                            stderr=PIPE)
        p.wait()
        #print "stdout: %s" % (p.stdout.readlines(), )
        #print "Erros: %s" % (p.stderr.readlines(), )

    def Merge(self, infile, outfile):
        sys.argv = [ infile[0], infile[1], infile[2], infile[3], '-o',outfile, '-a_nodata', '-999']
        gm.main()


"""

limage = Index("/home/faizan/HDD1/EVI/2005/MODIS.EVI.2005004.h23v06.tif")
A2001001.h23v06.Land_Cover_Type_2.uni
fill=-999
years=[2001, 2007]
shape="/home/faizan/Pakistan/pakistan shape file/PAK_adm0.shp"

files=[]
for n in range(len(years)):
    year=years[n]
    for i in range(1, 363):
        files=[]
        for V in range(5,7):
            for H in range(23,25):
                files.append("/home/faizan/HDD1/EVI/"+str(year)+"/MODIS.EVI.%d%03d"  % (year, i)+ ".h%dv%02d" % (H,V) + ".tif" )
        merge="/home/faizan/HDD1/EVI/"+str(year)+"/mosaic.%d%03d"  % (year, i) + ".tif"
        limage.MergeWithGdalwarp(files, merge)
        clip="/home/faizan/HDD1/EVI/"+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        limage.ClipWithGdalwarp(merge, clip, shape)
"""
"""
#/home/faizan/USA_data/8days/pak_lcd/A2001001.h23v06.Land_Cover_Type_2.uni

limage = Index("/home/faizan/USA_data/8days/pak_lcd/A2001001.h23v06.Land_Cover_Type_1.uni.tif")
fill=-999
years=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
shape="/home/faizan/Pakistan/pakistan shape file/PAK_adm0.shp"

files=[]
for n in range(len(years)):
    year=years[n]
    for i in range(1, 2):
        files=[]
        for V in range(5,7):
            for H in range(23,25):
                files.append("/home/faizan/USA_data/8days/pak_lcd/A%d%03d"  % (year, i)+ ".h%dv%02d" % (H,V) + ".Land_Cover_Type_1.uni.tif" )
        merge="/home/faizan/USA_data/8days/pak_lcd/mosaic.%d%03d" % (year, i) + ".Type1.tif"
        limage.MergeWithGdalwarp(files, merge)
        clip="/home/faizan/USA_data/8days/pak_lcd/clip.%d%03d"  % (year, i) + ".Type1.tif"
        limage.ClipWithGdalwarp(merge, clip, shape)

"""
limage = Index("/home/faizan/Pakistan/EVI/2008/clip.2008002.tif")
#years=[2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
shape="/home/faizan/Desktop/shapefile/faislabad.shp"
for n in range(2002,2015):
    year=n
    for i in range(1, 363):
        full="/home/faizan/Pakistan/EVI/"+str(year)+"/clip.%d%03d"  % (year, i) + ".tif"
        clip="/home/faizan/Pakistan/EVI/"+str(year)+"/faislabad.%d%03d"  % (year, i) + ".tif"
        limage.ClipWithGdalwarp(full, clip, shape)