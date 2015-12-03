#!/bin/sh

for data in tmp dtr wet vap
do
for input in `ls /home/faizan/HDD1/anomaly/cru_pak.*.${data}.anomaly.tif`
do
output=`basename ${input} | awk -F . '{print "/home/faizan/HDD1/anomaly/"$1"."$2"."$3"."$4"."$5".sindh.tif"}'`
gdalwarp -overwrite -dstnodata -9999 -q -t_srs EPSG:4326 -ts 9 10 -r near -cutline ~/Desktop/shapefile/sindh.shp -crop_to_cutline ${input}  ${output}
echo ${input} "->" ${output}
done
done
