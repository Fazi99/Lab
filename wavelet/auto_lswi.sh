#!/bin/sh

area=${2}

for year in ${1}
do
  echo ${year}
  scp keniis:/media/Data/Data/Satellite/Pakistan_evi_lswi/A${year}*${area}.lswi.tif /dias/users/kuwata.k.u-tokyo/Data/MODIS/LSWI/
  for i in `ls /dias/users/kuwata.k.u-tokyo/Data/MODIS/LSWI/A${year}*.lswi.tif`
  do
    new=`basename ${i} .tif | awk -F . '{print "/dias/users/kuwata.k.u-tokyo/Data/MODIS/LSWI/MOD09A1."$1".LSWI.tif"}'`
    mv ${i} ${new}
  done
  python multi_lswi.py ${year}
  python convert_nmpy2tiff_lswi.py ${year}
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/numpy/*.npy
  for i in `ls /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/MODIS.LSWI.${year}*.tif`
  do
    new=`basename ${i} .tif | awk '{print "/dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/"$1"'.${area}'.tif"}'`
    mv ${i} ${new}
  done
  scp /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/*.tif keniis:/media/Data/Data/Satellite/MODIS_wavelet/${year}/
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/LSWI/*.tif
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/*.tif
done
