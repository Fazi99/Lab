#!/bin/sh

# MAKE LIST FILE
for file in ls -1 MOD09GA.*.hdf 
do
#input=`echo ${file} | awk -F . '{print $1"."$2"."$3"."$4"."$5}'`
output=`echo ${file} | awk -F . '{print $2}'`
# MRT MOSAIC
#mrtmosaic -i list1.txt -s 1111111111111111 -o ${output}.hdf

# RESAMPLING HDF FILE
#resample -p template.prm -i ${input}.hdf -o ~/Pakistan/Tera/bands/${output}.hdr
HDR=$output
# GET PARAMETER OF RESAMPLING
n=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep UR_CORNER_XY | awk '{print $6}'`
s=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep LL_CORNER_XY | awk '{print $6}'`
e=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep UR_CORNER_XY | awk '{print $5}'`
w=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep LL_CORNER_XY | awk '{print $5}'`
colnum=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep NSAMPLES | awk '{print $4}'`
rownum=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep NLINES | awk '{print $4}'`
null=`cat ~/Pakistan/Tera/bands/${HDR}.hdr | grep BACKGROUND_FILL | awk '{print $4}'`
# IMPORTING DAT FILE INTO GRASS
#echo $n,$s,$e,$w,$colnum,$rownum,$null
#echo "Which Band You want to open in Grass (write 1 , 2 etc) "
#read input_variable
band1=sur_refl_b01_1
raster=T${output}.1
r.in.bin input=${HDR}.$band1.dat output=$raster north=${n} south=${s} east=${e} west=${w} cols=${colnum} rows=${rownum} byte=2 anull=${null} --o
r.mapcalc "$raster= if($raster<=16000 & $raster>=-100, $raster*.0001)"
band2=sur_refl_b02_1
raster=T${output}.2
r.in.bin input=${HDR}.$band2.dat output=$raster north=${n} south=${s} east=${e} west=${w} cols=${colnum} rows=${rownum} byte=2 anull=${null} --o
r.mapcalc "$raster= if($raster<=16000 & $raster>=-100, $raster*.0001)"
band3=sur_refl_b03_1
raster=T${output}.3
r.in.bin input=${HDR}.$band3.dat output=$raster north=${n} south=${s} east=${e} west=${w} cols=${colnum} rows=${rownum} byte=2 anull=${null} --o
r.mapcalc "$raster= if($raster<=16000 & $raster>=-100, $raster*.0001)"
band4=sur_refl_b04_1
raster=T${output}.4
r.in.bin input=${HDR}.$band4.dat output=$raster north=${n} south=${s} east=${e} west=${w} cols=${colnum} rows=${rownum} byte=2 anull=${null} --o
r.mapcalc "$raster= if($raster<=16000 & $raster>=-100, $raster*.0001)"
band6=sur_refl_b06_1
raster=T${output}.6
r.in.bin input=${HDR}.$band6.dat output=$raster north=${n} south=${s} east=${e} west=${w} cols=${colnum} rows=${rownum} byte=2 anull=${null} --o
r.mapcalc "$raster= if($raster<=16000 & $raster>=-100, $raster*.0001)"
done
#d.mon x0








#d.erase
#g.region rast=$raster
#d.rast $raster
#d.legend $raster


#r.mapcalc "NDVI=(test1_o2-test1_o)/(test1_o2+test1_o)"rast.d.mon


