# -*- coding: utf-8 -*-
# 2015.03.06 K. Kuwata
# GetValue.py
"""
    画像から値を取得する
"""

__author__ = 'ken'

from lib.GdalHandle import GImage

image = GImage("/home/faizan/USA_data/8days/pakistan8days/A2001177.evi.tif")
#image = GImage("/home/faizan/USA_data/8days/pakistan8days/A2000073.evi.tif")
#image = GImage("/home/faizan/USA_data/flood_june2008/A2008153h10v05.sur_refl_b03.tif")
#image = GImage("/home/faizan/USA_data/8days/MODIS_merge/MOD09A1.A2000057.Merge.b01.tif")
value = image.GetValue(27.6570, 69.9482)
#value = image.GetValue(24.6526, 71.0797)
#value = image.GetValue(34.0470, -90.8445)
#value = image.GetValue(37.0577, -88.5100)
print value
