from lcd import Index


fill=255
path="/home/faizan/USA_data/8days/pak_lcd/"
with open('/home/faizan/USA_data/8days/pak_lcd/list.txt',"r") as f:
    #g=len(f.readlines())     #print sum(1 for _ in f)
    for line in f:
        l= line.split(".")
        #assigning names
        lcd_in=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".tif"
        lcd_ou=path+str(l[0])+"."+str(l[1])+"."+str(l[2])+".uni.tif"
        #mlswi=str(l[1])+".US"+".mlswi.tif"


        # loading images
        #red band
        limage = Index(lcd_in)
        # Get a pixel column number
        cols = limage.iminfo['cols']
        # Get pixel row number
        rows = limage.iminfo['rows']
        # Get pixel data as array
        lcd = limage.Band2Array()

        #calculate Flood
        LCD= (limage.CalcLCD(lcd, fill))
        #Get Flood as tiff
        limage.WriteArrayAsImage(lcd_ou, LCD)
        del lcd, LCD
f.close()

