# -*- coding: utf-8 -*-
# 2015.02.06 K. Kuwata
# calc_evi.py
__author__ = 'ken'

from CalcEVI import CalcVI_MODIS
import os
from glob import glob

cdir = os.getcwd()

mod09a1_dir = "/".join(cdir.split('/')[:-2]) + "/MOD09A1/"
evi_dir = "/".join(cdir.split('/')[:-2]) + "/EVI/"

blue_paths = sorted(glob(mod09a1_dir + "*b03.tif"))
green_paths = sorted(glob(mod09a1_dir + "*b04.tif"))
red_paths = sorted(glob(mod09a1_dir + "*b01.tif"))
nir_paths = sorted(glob(mod09a1_dir + "*b02.tif"))

for (blue_path, red_path, nir_path) in zip(blue_paths,
                                         red_paths,
                                         nir_paths):
    EVI = CalcVI_MODIS(blue_path, red_path, nir_path)
    outpath = evi_dir + ".".join(blue_path.split('/')[-1].split('.')[0:2]) + \
              ".EVI.tif"
    EVI.EVI_TIFF(outpath)
    print "Calculated EVI: %s" % (outpath)
