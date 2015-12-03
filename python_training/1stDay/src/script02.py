# -*- coding: utf-8 -*-
# script02.py
# 2014.10.26 K. Kuwata

from wavelet import wavelet_jsm

def main():
    while True:
        try:
            year = int(raw_input("Please enter year: "))
            sc = int(raw_input("Please enter securities code: "))
            print "Downloading stock data of SC:%s" % (sc)
            wjs = wavelet_jsm(sc, year)
            dates, values = wjs.GetStockValue()
            svalues = wjs.denoise(values)
            wjs.graph_smooth(dates, values, svalues)
        except:
            print "Ooops! Maybe, securities code is wrong... Try again..."

if __name__=="__main__":
    main()

