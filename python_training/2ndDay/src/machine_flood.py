from machine import Index
import numpy as np
from sklearn import svm
from osgeo import gdal


fill=-999
path="/home/faizan/Desktop/full/"

#assigning names training data

Tevi=path+"evi_t.tif"
Tdvel=path+"dvel_t.tif"
Tlswi=path+"lswi_t.tif"
Tflood=path+"flood_t.tif"

#assigning names test data
evi=path+"A2014257.evi.tif"
dvel=path+"A2014257.dvel.tif"
lswi=path+"A2014257.lswi.tif"
Oflood = path+"A2014257.machineflood.tif"

#loading image training
limage = Index(Tevi)
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
EVI_t = (limage.index2Array(fill))

limage = Index(Tlswi)
LSWI_t = (limage.index2Array(fill))

limage = Index(Tdvel)
DVEL_t = (limage.index2Array(fill))

limage = Index(Tflood)
Flood_t = (limage.index2Array(fill))

# arranging training data
X = (limage.trtData(EVI_t, LSWI_t, DVEL_t))
Y = (limage.trainResult(Flood_t))
# SVM machine learning
clf = svm.SVC()
clf = clf.fit(X,Y)

#del EVI_t, LSWI_t, DVEL_t, Flood_t, X, Y
#Test data

limage = Index(evi)
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
EVI = (limage.index2Array(fill))

limage = Index(lswi)
LSWI = (limage.index2Array(fill))

limage = Index(dvel)
DVEL = (limage.index2Array(fill))

# arranging test data
data = (limage.trtData(EVI, LSWI, DVEL))

#output result
flood = clf.predict(data)
#Get Flood as tiff
limage.WriteArrayAsImage(Oflood, flood)
del flood, EVI, LSWI, DVEL, data







