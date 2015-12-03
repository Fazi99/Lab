#!/bin/sh

#echo "enter year"
#read input_variable
#year=$input_variable

dummy01="/home/faizan/Pakistan/EVI/resample/dummy01.tif"
dummy02="/home/faizan/Pakistan/EVI/resample/dummy02.tif"

for year in 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014
do
for i in `seq -w 1 363`
do
  for input in `ls /home/faizan/Pakistan/EVI/${year}/clip.${year}$i.tif`
  #for input in `ls /home/faizan/Pakistan/EVI/2002/sindh.*.${data}"_avg_evi_value".tif`
  do

    output=`basename ${input} | awk -F . '{print "/home/faizan/Pakistan/EVI/resample/pak_crop_evi."$2".5km.tif"}'`
    gdal_translate -of GTIFF -projwin 67.0185470581053977 34.7181701660155611 74.9403533935546733 23.7029151916504972  ${input} ${dummy01}

    gdalwarp -overwrite -q -dstnodata -9999 -t_srs EPSG:4326 -ts 158 220 -r near ${dummy01} ${dummy02}
    
    /usr/bin/gdal_calc.py \
      -A /home/faizan/Desktop/pakistan_grid_5km.tif \
      -B ${dummy02} \
      --outfile=${output} \
      --NoDataValue=-9999 \
      --calc="B*(A>=0)"
  done
  echo Finish ${year}
done
done

rm ${dummy01} ${dummy02}
