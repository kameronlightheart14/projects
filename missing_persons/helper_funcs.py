
import numpy as np
import os
from topo_tools import topo_tools


def spar(filepath):
    data = np.load(filepath)
    mask = data == 0
    #mask2 = -mask
    return len(data[mask]) / np.prod(data.shape)

def search():
    paths = ['2020-02-27_15:06_2_5_10_100/BOX' + str(i) + '_ADJ.npy' for i in range(36)]

    for path in paths:
        print(spar(path))


def search_all():
    dirs        = os.listdir()
    search_dirs = []
    maxs        = []


    #Get each directory with data in it
    for dir in dirs:
        if '2020' in dir:
            search_dirs.append(dir)

    # for each data directory, get the files and
    # get the maximum number of ADJ files
    for dir in search_dirs:
        files  = os.listdir(path=dir)
        counts = []
        for file in files:
            if 'ADJ' in file:
                box,end = file.split('_')
                counts.append(int(box[3:]))
        if len(counts) == 0:
            max_ = -1
            maxs.append(max_)
        else:
            max_ = max(counts)
            maxs.append(max_)

    # now get the sparsities for each directory
    for i,dir in enumerate(search_dirs):
        index = maxs[i]
        spars = []
        if index >0:
            files = [dir + '/BOX' + str(j) + '_ADJ.npy' for j in range(index)]
            for file in files:
                spars.append(spar(file))
        elif index ==0:
            spars.append(spar(dir + '/BOX0_ADJ.npy'))
        else:
            spars.append(-1)

        if index == 0:
            avg = spars
        else:
            avg = np.mean(spars)
        print(dir, 'Sparcity', avg)


def get_obj(index):
    dir = '2020-03-28_17.26_16_5_10_100/BOX' + str(index)
    end = ['_topo.npy','_lons.npy','_lats.npy']
    params = [dir + e for e in end ]

    obj = topo_tools(*params)

    return obj

def plot_walkers(index,w,t):
    obj = get_obj(index)
    obj.gen_walkers(obj.bbox,walkers=w,time=t, plot=True)
