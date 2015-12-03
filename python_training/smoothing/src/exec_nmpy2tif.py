# -*- coding: utf-8 -*-
# 2015.02.15 K. Kuwata
# exec_nmpy2tif.py
"""
    numpy arrayをTiff画像へ変換
    範囲は、イリノイ州周辺
"""

__author__ = 'ken'

from lib.array2tiff import na2tiff
from lib.projectmanage import Manage
from glob import glob
import numpy as np
from os.path import split, splitext
manage = Manage("smoothing")

numpypath = manage.nmpypath
modpath = manage.projectpath + "/MOD09A1/*tif"
tifpath = manage.projectpath + "/tiff/"

filelists = sorted(glob(numpypath + "MODIS.EVI.*.npy"))

ref_image = glob(modpath)[0]

tiff = na2tiff(ref_image)

for nmpy in filelists:
    outpath = tifpath + splitext(split(nmpy)[1])[0] + ".tif"
    array = np.load(nmpy)
    tiff.Array2Tiff(outpath, array)
    print "%s is converted into Tiff!" % (nmpy)
