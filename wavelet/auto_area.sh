#!/bin/sh

area=${2}

for year in ${1}
do
  echo ${year}
  scp keniis:/media/Data/Data/Satellite/Pakistan_evi_lswi/A${year}*${area}.evi.tif /dias/users/kuwata.k.u-tokyo/Data/MODIS/EVI/
  for i in `ls /dias/users/kuwata.k.u-tokyo/Data/MODIS/EVI/A${year}*.evi.tif`
  do
    new=`basename ${i} .tif | awk -F . '{print "/dias/users/kuwata.k.u-tokyo/Data/MODIS/EVI/MOD09A1."$1".EVI.tif"}'`
    mv ${i} ${new}
  done
  python multi.py ${year}
  python convert_nmpy2tiff.py ${year}
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/numpy/*.npy
  for i in `ls /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/MODIS.EVI.${year}*.tif`
  do
    new=`basename ${i} .tif | awk '{print "/dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/"$1"'.${area}'.tif"}'`
    mv ${i} ${new}
  done
  scp /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/*.tif keniis:/media/Data/Data/Satellite/MODIS_wavelet/${year}/
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/EVI/*.tif
  rm /dias/users/kuwata.k.u-tokyo/Data/MODIS/tif/*.tif
done
