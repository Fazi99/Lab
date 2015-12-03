# -*- coding: utf-8 -*-
# 2015.03.06 K. Kuwata
# GetValue.py
"""
    画像から値を取得する
"""

__author__ = 'ken'


lat = 28.13753
lon = 68.51805
path="/home/faizan/USA_data/8days/pakistan8days/"

#output files
NDVI=path+"NDVI.txt"
EVI=path+"EVI.txt"
LSWI=path+"LSWI.txt"
DVEL=path+"DVEL.txt"
FLOOD=path+"FLOOD.txt"

#opening files
O_ndvi = open(NDVI, "r+")
O_evi = open(EVI, "r+")
O_lswi = open(LSWI, "r+")
O_dvel = open(DVEL, "r+")
O_flood = open(FLOOD, "r+")


with open('/home/faizan/USA_data/8days/pakistan8days/list1.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split()
        #assigning names
        ndvi=path+str(l[0])+".ndvi.tif"
        evi=path+str(l[0])+".evi.tif"
        lswi=path+str(l[0])+".lswi.tif"
        dvel=path+str(l[0])+".dvel.tif"
        flood=path+str(l[0])+".flood.tif"
        NDVI=path+"NDVI.txt"
        EVI=path+"EVI.txt"
        LSWI=path+"LSWI.txt"
        DVEL=path+"DVEL.txt"
        FLOOD=path+"FLOOD.txt"

        from lib.GdalHandle import GImage

        #NDVI
        image = GImage(ndvi)
        value = image.GetValue(lat, lon)
        O_ndvi.write(str(l[0])+","+str(value)+"\n")


        #EVI
        image = GImage(evi)
        value = image.GetValue(lat, lon)
        O_evi.write(str(l[0])+","+str(value)+"\n")

        #LSWI
        image = GImage(lswi)
        value = image.GetValue(lat, lon)
        O_lswi.write(str(l[0])+","+str(value)+"\n")

        #DVEL
        image = GImage(dvel)
        value = image.GetValue(lat, lon)
        O_dvel.write(str(l[0])+","+str(value)+"\n")

        #FLOOD
        image = GImage(flood)
        value = image.GetValue(lat, lon)
        O_flood.write(str(l[0])+","+str(value)+"\n")


f.close()
O_ndvi.close()
O_evi.close()
O_lswi.close()
O_dvel.close()
O_flood.close()
