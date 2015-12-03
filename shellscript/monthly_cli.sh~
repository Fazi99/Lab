#!/bin/sh

dummy01="/home/faizan/HDD1/EVI/resample/dummy01.tif"
dummy02="/home/faizan/HDD1/EVI/resample/dummy02.tif"

for data in tmx tmn pet pre
do
for input in `ls /home/faizan/HDD1/anomaly/cru.*.${data}.anomaly.tif`
do
    output=`basename ${input} | awk -F . '{print "/home/faizan/HDD1/climate_resample/"$1"."$2"."$3"."$4"."$5".pak_crop_50km.tif"}'`

    gdal_translate -of GTIFF -projwin 67.0185470581053977 34.7181701660155611 74.9403533935546733 23.7029151916504972  ${input} ${dummy01}

    gdalwarp -overwrite -q -dstnodata -999 -t_srs EPSG:4326 -ts 158 220 -r near ${dummy01} ${dummy02}
    
    /usr/bin/gdal_calc.py \
      -A /home/faizan/Desktop/pakistan_grid_5km.tif \
      -B ${dummy02} \
      --outfile=${output} \
      --NoDataValue=-9999 \
      --calc="B*(A>=0)"
  done
  echo Finish ${year}
done

rm ${dummy01} ${dummy02}

