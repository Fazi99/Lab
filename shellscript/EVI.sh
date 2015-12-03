#!/bin/sh

for data in Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec
do
for input in `ls /home/faizan/HDD1/EVI/2014/Pak_crop.*.${data}"_avg_evi_value".tif`
#for input in `ls /home/faizan/Pakistan/EVI/2002/sindh.*.${data}"_avg_evi_value".tif`
do
output=`basename ${input} | awk -F . '{print "/home/faizan/HDD1/EVI/2014/"$1"."$2"."$3".sindh2.tif"}'`
#gdalwarp -overwrite -dstnodata -9999 -q -t_srs EPSG:4326 -ts 9 10 -r near  ${input}  ${output}
gdalwarp -overwrite -dstnodata -9999 -q -t_srs EPSG:4326 -ts 9 10 -r near -cutline ~/Desktop/shapefile/sindh.shp -crop_to_cutline  ${input}  ${output}
echo ${input} "->" ${output}

done
done


