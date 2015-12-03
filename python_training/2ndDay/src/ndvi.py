from osgeo import gdal
import numpy
from numpy.core.umath import add, subtract
import datetime
import math

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

    def Band2Array(self,factor,fill):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        band = self.ds.GetRasterBand(1)
        self.factor= factor
        self.fill=fill
        array = band.ReadAsArray(0, 0, cols, rows)
        array [array <-100] =fill
        array [array >16000] =fill
        array = numpy.where(array ==fill, fill , array * 0.0001)
        return  array

    def WriteArrayAsImage(self, out_fname, outArray):
        cols = self.iminfo['cols']
        rows = self.iminfo['rows']
        driver = self.ds.GetDriver()
        outDS = driver.Create(out_fname, cols, rows, 3, gdal.GDT_Float32)
        outDS.SetGeoTransform(self.ds.GetGeoTransform())
        outDS.SetProjection(self.ds.GetProjection())
        outBand = outDS.GetRasterBand(1)
        outBand.WriteArray(outArray)
        outDS = None
        del outDS, outBand
    def CalcNDVI ( self , NIR , Red, fill):
        Ndvi_lower = numpy.where (NIR == fill, fill , add (NIR , Red))
        Ndvi_upper = numpy.where (NIR == fill, fill ,subtract (NIR , Red))
        #Mask = Numpy.Greater (Ndvi_lower, 0)
        Ndvi_lower = numpy.where (Ndvi_lower == 0 , fill , Ndvi_lower)
        NDVI = numpy.where (Ndvi_lower == fill , fill , Ndvi_upper/Ndvi_lower)
        return NDVI
    def CalcEVI ( self , NIR , Red , Blue, fill ):
        #for cloud-cover  blue >= 0.27
        Blue [Blue >= 0.27] = fill
        Evi_upper = numpy.where (Blue == fill , fill , 2.5 *  subtract (NIR , Red))
        Evi_lower = numpy.where (Blue == fill , fill , (NIR + (6 * Red) - (7.5 * Blue) + 1))
        Evi_lower = numpy.where (Evi_lower == 0 , fill , Evi_lower)
        EVI = numpy.where(Evi_lower == fill , fill , Evi_upper/Evi_lower)
        EVI [EVI <= 0] = fill
        EVI [EVI >= 1] = fill
        #EVI = 2.5 * (NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1) * mask
        return EVI
    def CalcLSWI (self, NIR, SWIR, Blue, fill):
        Blue [Blue >= 0.27] = fill
        Swir_lower=numpy.where(Blue == fill, fill , add(NIR, SWIR))
        Swir_upper=numpy.where(Blue == fill, fill , subtract(NIR, SWIR))
        Swir_lower=numpy.where(Swir_lower ==0 , fill, Swir_lower)
        LSWI=numpy.where(Swir_lower==fill, fill ,Swir_upper/Swir_lower)
        return LSWI
    def CalcDVEL(self, EVI, LSWI, fill):

        DVEL=numpy.where(LSWI == fill, fill , subtract(EVI,LSWI))
        return DVEL
    def CalcFlood(self, EVI, LSWI, DVEL):
        #NDVI[[EVI<=0.3] & [DVEL<=0.05]] = 1
        #NDVI[[EVI<=0.05] and [LSWI<=0.0999]]=1
        EVI_1 = numpy.where(EVI<=0.3, 1,0)
        DVEL_1 = numpy.where(DVEL<=0.05,1,0)
        combine =EVI_1+DVEL_1
        check1 = numpy.where(combine==2, 1,0)
        EVI_2 = numpy.where(EVI<=0.05, 1,0)
        LSWI_2 = numpy.where(LSWI<=0.0999,1,0)
        combine=EVI_2+LSWI_2
        check2 = numpy.where(combine==2, 1,0)
        combine = check1 + check2
        flood = numpy.where(combine==2, 1, combine)
        return flood




# Calculating reflectance of Band3


fill=-999
limage = Index("/home/faizan/Pakistan/python/all.sur_refl_b01_1.tif")

# Get a pixel column number
cols = limage.iminfo['cols']
# Get pixel row number
rows = limage.iminfo['rows']

# Get pixel data as array
red = (limage.Band2Array(0.0001, fill))

#limage.WriteArrayAsImage("1.tif", red)

limage = Index("/home/faizan/Pakistan/python/all.sur_refl_b02_1.tif")
# Get pixel data as array
nir = (limage.Band2Array(0.0001, fill))

limage = Index("/home/faizan/Pakistan/python/all.sur_refl_b03_1.tif")
# Get pixel data as array
blue = (limage.Band2Array(0.0001, fill))
limage = Index("/home/faizan/Pakistan/python/all.sur_refl_b06_1.tif")
# Get pixel data as array
SWIR = (limage.Band2Array(0.0001, fill))
#GET NDVI as tiff
NDVI= limage.CalcNDVI(nir,red, fill)
limage.WriteArrayAsImage("NDVItest.tif", NDVI)
#GET EVI as tiff
EVI= limage.CalcEVI(nir,red,blue,fill)
limage.WriteArrayAsImage("EVItest.tif", EVI)
#Get LSWI as tiff
LSWI= (limage.CalcLSWI(nir, SWIR, blue, fill))
limage.WriteArrayAsImage("LSWItest.tif", LSWI)
#Get DVEL as tiff
DVEL= (limage.CalcDVEL(EVI, LSWI, fill))
limage.WriteArrayAsImage("DVELtest.tif", DVEL)
#Get Flood as tiff
Flood= (limage.CalcFlood(EVI, LSWI, DVEL))
limage.WriteArrayAsImage("Floodtest.tif", Flood)

#limage = Index("/home/faizan/Pakistan/python/band2nir.sur_refl_b02_1.tif")
#check2 = (limage.Band2Array())
#check2  = numpy.where(check2 <= -100 , None , check2)
#print "JJJJJJJJJJJ"
#print check2
#my_file = open("/home/faizan/test.txt", "w")
#my_file.write(str(check2))
#my_file.close()
#check3 = check1+check2
#print "JJJJJJJJJJJ"
#print check3
#check3 = check1*check2
#print "JJJJJJJJJJJ"
#print check3
#check3 = check1-check2
#print "JJJJJJJJJJJ"
#print check3
 # Get information from a parameter file
#Parameters = limage.ReturnParameters()
#print Parameters
 # Calculate Radiance from DN
#Radiance = limage.DN2Radiance(array, Parameters)
 # Calculate Reflectance from Radiance
#Reflectance4 = limage.Radiance2Reflectance(Radiance, Parameters)

# Calculating NDVI
 # Get a pixel column number
#cols = limage.iminfo['cols']
 # Get pixel row number
#rows = limage.iminfo['rows']

 # Calculate NDVI
#NDVI = limage.CalcNDVI(NIR=Reflectance4.reshape(cols * rows), Red=Reflectance3.reshape(cols * rows))

 # Make a Geotiff file
#limage.WriteArrayAsImage("NDVI.tif", NDVI.reshape(rows, cols))


# Make a Geotiff file
#limage.WriteArrayAsImage("Reflectance_B3.tif", Reflectance3)
