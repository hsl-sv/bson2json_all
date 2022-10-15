# not tested

import glob
import json
import pathlib

florig = glob.glob('D:/UWO/unpack/NonUFS_221015/cms/**/*.json')
flmod = glob.glob('D:/UWO/unpack/NonUFS/cms/**/*.json')

diff = lambda l1,l2: [x for x in l1 if x not in l2]

for (j, fid) in enumerate(florig):
    fname = pathlib.Path(fid).stem
    fid_orig = open(fid, 'r', encoding='utf-8') 
    fid_mod = open(flmod[j], 'r', encoding='utf-8')
    j1 = json.load(fid_orig)
    j2 = json.load(fid_mod)
    fid_orig.close()
    fid_mod.close()

    # diff
    if j1 is not None and j2 is not None:
        d1_2 = diff(j1, j2)
        d2_1 = diff(j2, j1)

    if len(d1_2) != 0:
        with open(fname + '_1_2.txt', 'w', encoding='utf-8') as fid_diff1_2:
            for (i, diff1_2) in enumerate(d1_2):
                fid_diff1_2.write(str(diff1_2) + '\n')

        fid_diff1_2.close()

    if len(d2_1) != 0:
        with open(fname + '_2_1.txt', 'w', encoding='utf-8') as fid_diff2_1:        
            for (i, diff2_1) in enumerate(d2_1):
                fid_diff2_1.write(str(diff2_1) + '\n')

        fid_diff2_1.close()