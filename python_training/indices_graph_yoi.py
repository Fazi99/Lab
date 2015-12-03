
"""

"""

__author__ = 'fazi'

import pandas as pd
import datetime
#%matplotlib inline
from matplotlib import pyplot as plt
import time as t

for i in range (83):
    evi_path= "/home/faizan/USA_data/h11v05/output_near/EVI.near%02d.csv" % i
    ndvi_path= "/home/faizan/USA_data/h11v05/output_near/NDVI.near%02d.csv"  % i
    lswi_path= "/home/faizan/USA_data/h11v05/output_near/LSWI.near%02d.csv" % i
    flood_path= "/home/faizan/USA_data/h11v05/output_near/FLOOD.near%02d.csv" % i
    palsar_path= "/home/faizan/USA_data/PALSAR/output/750backscatter%02d.csv" % i
    pic_path = "/home/faizan/USA_data/graphs/US_near_pt_%02d.png" % i
    title= "Time series of vegetation indices at point US_near_pt_%02d" % i

    data = pd.read_csv(evi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    dummy = data[data.index.year > 2004]
    dummy = dummy[dummy.index.year<2009]
    time = dummy.index[dummy[1] > -999]
    evi = dummy[1][dummy[1]>-999]

    data = pd.read_csv(ndvi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    dummy = data[data.index.year > 2004]
    dummy = dummy[dummy.index.year<2009]
    time1 = dummy.index[dummy[1] > -999]
    ndvi = dummy[1][dummy[1]>-999]

    data = pd.read_csv(lswi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    dummy = data[data.index.year > 2004]
    dummy = dummy[dummy.index.year<2009]
    time2 = dummy.index[dummy[1] > -999]
    lswi = dummy[1][dummy[1]>-999]

    data = pd.read_csv(flood_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    dummy = data[data.index.year > 2004]
    dummy = dummy[dummy.index.year<2009]
    time3 = dummy.index[dummy[1] > -999]
    flood = dummy[1][dummy[1]>-999]

    data = pd.read_csv(palsar_path)
    dates = [datetime.datetime.strptime(str(i[:10]), "%Y-%m-%d") for i in data["3"]]
    data.index = dates
    time4= data.index[data["0"] == "HH"]
    bs_hh = data["2"][data["0"] == "HH"]
    time5= data.index[data["0"] == "HV"]
    bs_hv = data["2"][data["0"] == "HV"]

    fig = plt.figure(figsize=(8,5))
    ax = fig.add_subplot(111)

    lns1 = ax.plot(time, evi, 'r', label = 'evi')
    lns2 = ax.plot(time2, lswi, 'b', label = 'lswi')
    lns3 = ax.plot(time1, ndvi, 'c', label = 'ndvi')
    lns4 = ax.plot(time3, flood, 'y', label = 'flood')
    ax2 = ax.twinx()
    lns5 = ax2.plot(time4, bs_hh , 'mo', label = 'bk_sct_hh')
    lns6 = ax2.plot(time5, bs_hv , 'go', label = 'bk_sct_hv')

    # added these lines
    lns = lns1+lns2+lns3+lns4+lns5+lns6
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=2, prop={'size':10})

    ax.grid()
    ax.set_title(title)
    ax.set_xlabel("Time (year)")
    ax.set_ylabel("evi, lswi, ndvi, flood")
    ax2.set_ylabel("backscatter")
    ax2.set_ylim(0, -40)
    ax.set_ylim(-0.5,1.2)
    fig.savefig(pic_path)



import pandas as pd
import datetime
#%matplotlib inline
from matplotlib import pyplot as plt
import time as t

for i in range (62):
    evi_path= "/home/faizan/USA_data/8days/pakistan8days/output_far/EVI.near%02d.csv" % i
    ndvi_path= "/home/faizan/USA_data/8days/pakistan8days/output_far/NDVI.near%02d.csv"  % i
    lswi_path= "/home/faizan/USA_data/8days/pakistan8days/output_far/LSWI.near%02d.csv" % i
    flood_path= "/home/faizan/USA_data/8days/pakistan8days/output_far/FLOOD.near%02d.csv" % i
    palsar_path= "/home/faizan/USA_data/PALSAR/output/550backscatter%02d.csv" % i
    pic_path = "/home/faizan/USA_data/graphs/Pak_all_far_pt_%02d.png" % i
    title= "All year Time series of vegetation indices at point Pak_far_pt_%02d" % i

    data = pd.read_csv(evi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    time=data.index[data[1] > -999]
    evi = data[1][data[1] > -999]

    data = pd.read_csv(ndvi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    time1=data.index[data[1] > -999]
    ndvi = data[1][data[1] > -999]

    data = pd.read_csv(lswi_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    time2=data.index[data[1] > -999]
    lswi = data[1][data[1] > -999]

    data = pd.read_csv(flood_path, header=None)
    dates = [datetime.datetime.strptime(str(i[1:]), "%Y%j") for i in data[0]]
    data.index = dates
    time3=data.index[data[1] > -999]
    flood = data[1][data[1] > -999]

    data = pd.read_csv(palsar_path)
    dates = [datetime.datetime.strptime(str(i[:10]), "%Y-%m-%d") for i in data["3"]]
    data.index = dates
    time4= data.index[data["0"] == "HH"]
    bs_hh = data["2"][data["0"] == "HH"]
    time5= data.index[data["0"] == "HV"]
    bs_hv = data["2"][data["0"] == "HV"]

    fig = plt.figure(figsize=(18,5))
    ax = fig.add_subplot(111)

    lns1 = ax.plot(time, evi, 'r', label = 'evi')
    lns2 = ax.plot(time2, lswi, 'b', label = 'lswi')
    lns3 = ax.plot(time1, ndvi, 'c', label = 'ndvi')
    lns4 = ax.plot(time3, flood, 'y', label = 'flood')
    ax2 = ax.twinx()
    lns5 = ax2.plot(time4, bs_hh , 'mo', label = 'bk_sct_hh')
    lns6 = ax2.plot(time5, bs_hv , 'go', label = 'bk_sct_hv')

    # added these lines
    lns = lns1+lns2+lns3+lns4+lns5+lns6
    labs = [l.get_label() for l in lns]
    ax.legend(lns, labs, loc=2, prop={'size':10})

    ax.grid()
    ax.set_title(title)
    ax.set_xlabel("Time (year)")
    ax.set_ylabel("evi, lswi, ndvi, flood")
    ax2.set_ylabel("backscatter")
    ax2.set_ylim(0, -40)
    ax.set_ylim(-0.5,1.2)
    fig.savefig(pic_path)





