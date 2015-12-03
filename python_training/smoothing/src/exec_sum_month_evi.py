# -*- coding: utf-8 -*-
# 2015.03.07 K. Kuwata
# exec_sum_month_evi.py
__author__ = 'ken'

from lib.projectmanage import Manage
from lib.GdalHandle import MultiImages

import datetime
from calendar import monthrange

manage = Manage("smoothing")

tifpath = manage.projectpath + "/tiff/"


for y in xrange(2001, 2011, 1):
    for m in xrange(1, 13, 1):
        start_date = datetime.date(y, m, 1)
        start_jdate = int(start_date.strftime('%j'))
        youbi, day = monthrange(y, m)
        end_date = datetime.date(y, m, day)
        end_jdate = int(end_date.strftime('%j'))
        if m == 12:
            end_jdate = 361
        inputlist = [tifpath + "MODIS.EVI.%d%03d.tif" % (y, i) for i in xrange(start_jdate, end_jdate + 1)]
        mimage = MultiImages(inputlist)
        out_name = tifpath + "MODIS.EVI.MonthlySum.%d%02d.tif" % (y, m)
        SumArray = mimage.SumAllArrays()
        mimage.Array2Tiff(out_name, SumArray)
        print "%d %d is done!" % (y, m)


