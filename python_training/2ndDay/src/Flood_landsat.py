from index_class_landsat import Index


fill=-999
path="/home/faizan/USA_data/landsat/3/"
with open('/home/faizan/USA_data/landsat/3/list.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split()
        #assigning names
        red_b=path+str(l[0])+"Reflectance_B3_B1.tif"
        nir_b=path+str(l[0])+"Reflectance_B4_B2.tif"
        blue_b=path+str(l[0])+"Reflectance_B1_B3.tif"
        swir_b=path+str(l[0])+"Reflectance_B5_B6.tif"
        ndvi=str(l[0])+"ndvi.tif"
        evi=str(l[0])+"evi.tif"
        lswi=str(l[0])+"lswi.tif"
        dvel=str(l[0])+"dvel.tif"
        flood=str(l[0])+"flood.tif"


        # loading images
        #red band
        limage = Index(red_b)
        # Get a pixel column number
        cols = limage.iminfo['cols']
        # Get pixel row number
        rows = limage.iminfo['rows']
        # Get pixel data as array
        red = (limage.Band2Array(0.0001, fill))

        # nir band
        limage = Index(nir_b)
        # Get pixel data as array
        nir = (limage.Band2Array(0.0001, fill))

        # blue band
        limage = Index(blue_b)
        # Get pixel data as array
        blue = (limage.Band2Array(0.0001, fill))

        #  swir band
        limage = Index(swir_b)
        # Get pixel data as array
        SWIR = (limage.Band2Array(0.0001, fill))

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
        #limage.WriteArrayAsImage(lswi, LSWI)


        #calculate DVEL
        DVEL= (limage.CalcDVEL(EVI, LSWI, fill))
        #Get DVEL as tiff
        #limage.WriteArrayAsImage(dvel, DVEL)

        #calculate Flood
        Flood= (limage.CalcFlood(EVI, LSWI, DVEL, fill))
        #Get Flood as tiff
        limage.WriteArrayAsImage(flood, Flood)
        del Flood, EVI, DVEL, NDVI, LSWI, red, blue, nir, SWIR
f.close()






 # Calculate NDVI
#NDVI = limage.CalcNDVI(NIR=Reflectance4.reshape(cols * rows), Red=Reflectance3.reshape(cols * rows))

 # Make a Geotiff file
#limage.WriteArrayAsImage("NDVI.tif", NDVI.reshape(rows, cols))


# Make a Geotiff file
#limage.WriteArrayAsImage("Reflectance_B3.tif", Reflectance3)
