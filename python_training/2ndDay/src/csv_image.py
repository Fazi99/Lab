from index_class import Index
import numpy as np

fill=-999
path="/home/faizan/Desktop/full/"

#assigning names
"""
b1=path+"band1.tif"
b2=path+"band2.tif"
b3=path+"band3.tif"
b4=path+"band4.tif"
b6=path+"ndvi.tif"
"""
evi=path+"A2014257.evi.tif"
dvel=path+"A2014257.dvel.tif"
lswi=path+"A2014257.lswi.tif"
#ndvi=path+"ndvi.tif"
flood=path+"A2014257.flood.tif"

"""
b1o=path+"band1.csv"
b2o=path+"band2.csv"
b3o=path+"band3.csv"
b4o=path+"band4.csv"
b6o=path+"ndvi.csv"
"""
evio=path+"evi1.csv"
dvelo=path+"dvel1.csv"
lswio=path+"lswi1.csv"
#ndvio=path+"ndvi.csv"
floodo=path+"flood1.csv"
"""
# loading images
#red band
limage = Index(b1)
# Get a pixel column number
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
# Get pixel data as array
data= (limage.Band2Array(0.0001, fill))
np.savetxt(b1o, data, delimiter=",")
# nir band
limage = Index(b6)
data= (limage.Band2Array(0.0001, fill))
np.savetxt(b6o, data, delimiter=",")
limage = Index(b2)
data= (limage.Band2Array(0.0001, fill))
np.savetxt(b2o, data, delimiter=",")
limage = Index(b3)
data= (limage.Band2Array(0.0001, fill))
np.savetxt(b3o, data, delimiter=",")
limage = Index(b4)
data= (limage.Band2Array(0.0001, fill))
np.savetxt(b4o, data, delimiter=",")
"""
limage = Index(evi)
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']
data = (limage.index2Array(0.0001, fill))
np.savetxt(evio, data, delimiter=",")
"""
limage = Index(ndvi)
data = (limage.index2Array(0.0001, fill))
np.savetxt(ndvio, data, delimiter=",")
"""
limage = Index(lswi)
data = (limage.index2Array(0.0001, fill))
np.savetxt(lswio, data, delimiter=",")
limage = Index(dvel)
data = (limage.index2Array(0.0001, fill))
np.savetxt(dvelo, data, delimiter=",")
limage = Index(flood)
data = (limage.index2Array(0.0001, fill))
np.savetxt(floodo, data, delimiter=",")
"""
# blue band
limage = Index(blue_b)
# Get pixel data as array
blue = (limage.Band2Array(0.0001, fill))

#  swir band
limage = Index(swir_b)
# Get pixel data as array
SWIR = (limage.Band2Array(0.0001, fill))
        #calculate Flood

Mlswi= (limage.CalcMLSWI(nir, SWIR, fill))
#Get Flood as tiff
limage.WriteArrayAsImage(mlswi, Mlswi)
del Mlswi, red, blue, nir, SWIR
"""
"""
        #calculate NDVI
        NDVI= limage.CalcNDVI(nir,red, fill)
        #GET NDVI as tiff
        limage.WriteArrayAsImage(ndvi, NDVI)

        #calculate EVI
        EVI= limage.CalcEVI(nir,red,blue,fill)
        #GET EVI as tiff
        limage.WriteArrayAsImage(evi, EVI)

        #calculate LSWI
        LSWI= (limage.CalcLSWI(nir, SWIR, blue, fill))
        #Get LSWI as tiff
        limage.WriteArrayAsImage(lswi, LSWI)

        #calculate DVEL
        DVEL= (limage.CalcDVEL(EVI, LSWI, fill))
        #Get DVEL as tiff
        limage.WriteArrayAsImage(dvel, DVEL)

        #calculate Flood
        Flood= (limage.CalcFlood(EVI, LSWI, DVEL, fill))
        #Get Flood as tiff
        limage.WriteArrayAsImage(flood, Flood)
        del Flood, EVI, DVEL, NDVI, LSWI, red, blue, nir, SWIR
"""








 # Calculate NDVI
#NDVI = limage.CalcNDVI(NIR=Reflectance4.reshape(cols * rows), Red=Reflectance3.reshape(cols * rows))

 # Make a Geotiff file
#limage.WriteArrayAsImage("NDVI.tif", NDVI.reshape(rows, cols))


# Make a Geotiff file
#limage.WriteArrayAsImage("Reflectance_B3.tif", Reflectance3)
