from index_class import Index


fill=-999
path="/home/faizan/USA_data/h11v05/"
with open('/home/faizan/USA_data/h11v05/list1.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split(".")
        #assigning names
        red_b=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".sur_refl_b01.tif"
        nir_b=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".sur_refl_b02.tif"
        blue_b=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".sur_refl_b03.tif"
        swir_b=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".sur_refl_b06.tif"
        ndvi=str(l[1])+".US"+".ndvi.tif"
        evi=str(l[1])+".US"+".evi.tif"
        lswi=str(l[1])+".US"+".lswi.tif"
        dvel=str(l[1])+".US"+".dvel.tif"
        flood=str(l[1])+".US"+".flood.tif"
        mlswi=str(l[1])+".US"+".mlswivalue.tif"


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
                #calculate Flood

        Mlswi= (limage.CalcMLSWI(nir, SWIR, fill))
        #Get Flood as tiff
        limage.WriteArrayAsImage(mlswi, Mlswi)
        del Mlswi, red, blue, nir, SWIR
f.close()
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
