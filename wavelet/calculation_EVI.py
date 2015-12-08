# -*- coding: utf-8 -*-
# 2015.06.06 K. Kuwata
# calculation_EVI.py
"""
    MODISデータでEVIを計算する
"""

from lib.CalcEVI import CalcVI_MODIS
import os

year = 2005

DATA = 'MODIS'

HOME = os.environ['HOME']

data_dir = HOME + "/Data/" + DATA

out_dir = data_dir + "/EVI/"



