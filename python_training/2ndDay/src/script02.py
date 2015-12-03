# -*- coding: utf-8 -*-
# script01.py
# 2014.11.20 K. Kuwata

__author__ = 'ken'

from osgeo import osr, gdal
import numpy
from matplotlib import pyplot as plt

def reproject_dataset ( dataset, \
                        pixel_spacing=0.463/100., \
                        wkt_from="+proj=sinu +R=6371007.181 +nadgrids=@null +wktext", epsg_to=4326 ):
    """
    A sample function to reproject and resample a GDAL dataset from within
    Python. The idea here is to reproject from one system to another, as well
    as to change the pixel size. The procedure is slightly long-winded, but
    goes like this:

    1. Set up the two Spatial Reference systems.
    2. Open the original dataset, and get the geotransform
    3. Calculate bounds of new geotransform by projecting the UL corners
    4. Calculate the number of pixels with the new projection & spacing
    5. Create an in-memory raster dataset
    6. Perform the projection
    """
    # Define the UK OSNG, see <http://spatialreference.org/ref/epsg/27700/>
    wgs84= osr.SpatialReference ()
    wgs84.ImportFromEPSG ( epsg_to )
    modis = osr.SpatialReference ()
    modis.ImportFromProj4( wkt_from )
    tx = osr.CoordinateTransformation ( modis, wgs84 )
    # Up to here, all  the projection have been defined, as well as a
    # transformation from the from to the  to :)
    # We now open the dataset
    g = gdal.Open ( dataset )
    # Get the Geotransform vector
    geo_t = g.GetGeoTransform ()
    print geo_t
    x_size = g.RasterXSize # Raster xsize
    y_size = g.RasterYSize # Raster ysize
    # Work out the boundaries of the new dataset in the target projection
    (ulx, uly, ulz ) = tx.TransformPoint( geo_t[0], geo_t[3])
    (lrx, lry, lrz ) = tx.TransformPoint( geo_t[0] + geo_t[1]*x_size, \
                                          geo_t[3] + geo_t[5]*y_size )
    # Now, we create an in-memory raster
    mem_drv = gdal.GetDriverByName( 'MEM' )
    # The size of the raster is given the new projection and pixel spacing
    # Using the values we calculated above. Also, setting it to store one band
    # and to use Float32 data type.
    dest = mem_drv.Create('', int((lrx - ulx)/pixel_spacing), \
                          int((uly - lry)/pixel_spacing), 1, gdal.GDT_Int16)
    # Calculate the new geotransform
    new_geo = ( ulx, pixel_spacing, geo_t[2], \
                uly, geo_t[4], -pixel_spacing )
    # Set the geotransform
    dest.SetGeoTransform( new_geo )
    dest.SetProjection ( wgs84.ExportToWkt() )
    # Perform the projection/resampling
    res = gdal.ReprojectImage( g, dest, \
                               modis.ExportToWkt(), wgs84.ExportToWkt(), \
                               gdal.GRA_NearestNeighbour )
    return dest

dataset = 'HDF4_EOS:EOS_GRID:"/home/faizan/China_land_cover/shellscript/MOD09A1.A2010153.h11v04.005.2010164034523.hdf":MOD_Grid_500m_Surface_Reflectance:sur_refl_b01'

dest = reproject_dataset(dataset)

newRasterfn="MOD09A1.A2010153.h11v04.005.2010164034523.tif"

cols = dest.RasterXSize
rows = dest.RasterYSize
array = numpy.array(dest.ReadAsArray() * 0.0001, dtype=numpy.float32)
driver = gdal.GetDriverByName('GTiff')
outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)

outRaster.SetGeoTransform(dest.GetGeoTransform())

outband = outRaster.GetRasterBand(1)

outband.WriteArray(array)

outRaster.SetProjection(dest.GetProjection())

outband.FlushCache()
print numpy.__version__

gdal_dataset = gdal.Open("/home/faizan/China_land_cover/shellscript/MOD09A1.A2010153.h11v04.005.2010164034523.hdf")
print gdal_dataset.GetSubDatasets()
toa_data = gdal.Open(dataset)
array = toa_data.ReadAsArray()
plt.imshow(array, interpolation='nearest', vmin=0, vmax=4000, cmap=plt.cm.gray)
plt.colorbar()
plt.show()
