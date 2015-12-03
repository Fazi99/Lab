from index_class_PALSAR_try import Index


fill=-999
path="/home/faizan/USA_data/PALSAR/data/"
with open('/home/faizan/USA_data/PALSAR/data/list.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split("-")
        #assigning names
        input1=path+"IMG-"+str(l[1])+"-"+str(l[2])+"-H1.tif"
        #nir_b=path+str(l[0])+"Reflectance_B4_B2.tif"
        #blue_b=path+str(l[0])+"Reflectance_B1_B3.tif"
        #swir_b=path+str(l[0])+"Reflectance_B5_B6.tif"
        #ndvi=str(l[0])+"ndvi.tif"
        #evi=str(l[0])+"evi.tif"
        #lswi=str(l[0])+"lswi.tif"
        #dvel=str(l[0])+"dvel.tif"
        output1=str(l[1])+"."+str(l[2])+".backscatter_bin.tif"


        # loading images
        #red band
        limage = Index(input1)
        # Get a pixel column number
        cols = limage.iminfo['cols']
        # Get pixel row number
        rows = limage.iminfo['rows']
        # Get pixel data as array
        Output = (limage.Band2Array(input1))
        #GET  as tiff
        limage.WriteArrayAsImage(output1, Output)

        del Output
f.close()






 # Calculate NDVI
#NDVI = limage.CalcNDVI(NIR=Reflectance4.reshape(cols * rows), Red=Reflectance3.reshape(cols * rows))

 # Make a Geotiff file
#limage.WriteArrayAsImage("NDVI.tif", NDVI.reshape(rows, cols))


# Make a Geotiff file
#limage.WriteArrayAsImage("Reflectance_B3.tif", Reflectance3)
