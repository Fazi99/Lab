# -*- coding: utf-8 -*-
# 2015.06.07 K. Kuwata

import numpy as np
import os, sys
from glob import glob
from osgeo import gdal
from lib.GdalHandle import GImage

HOME = os.environ['HOME']
DATA = "MODIS"

argvs = sys.argv
year = argvs[1]
print year

nmpy_dir = HOME + "/Data/" + DATA + "/numpy"

tif_dir = HOME + "/Data/" + DATA + "/tif"

evi_dir = HOME + "/Data/" + DATA + "/EVI"


input_files = sorted(glob(nmpy_dir + "/MODIS.EVI." + str(year) + "*.npy"))


tiff = glob(evi_dir + "/*.tif")[0]

image = GImage(tiff)

cols = image.ds.RasterXSize
rows = image.ds.RasterYSize

for input_file in input_files:
    output_file = tif_dir + "/" + \
        os.path.splitext(os.path.split(input_file)[1])[0] \
        + ".tif"
    print output_file
    array = np.load(input_file)
    image.Array2Tiff(output_file, array.reshape(rows, cols))


