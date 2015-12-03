"""
for data in tmx tmn pet pre
do
for input in `ls /media/Data/Data/CRU/anomaly/cru.*.${data}.anomaly.tif`
do
output=`basename ${input} | awk -F . '{print "/home/ken/Data/CRU/resample/"$1"."$2"."$3"."$4"."$5".resample.tif"}'`
gdalwarp -overwrite -q -dstnodata -9999 -t_srs EPSG:4326 -ts 1440 720 -r near ${input}  ${output}
echo ${input} "->" ${output}
done
done

for data in tmx tmn pet pre
do
for input in `ls /home/faizan/HDD1/anomaly/cru_pak.*.${data}.anomaly.tif`
do
output=`basename ${input} | awk -F . '{print "/home/faizan/HDD1/anomaly/"$1"."$2"."$3"."$4"."$5".sindh.tif"}'`
gdalwarp -overwrite -q -dstnodata -9999 -t_srs EPSG:4326 -ts 1440 720 -r near ${input}  ${output}
echo ${input} "->" ${output}
done
done

"""
