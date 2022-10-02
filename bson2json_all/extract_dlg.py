import enum
import json
import glob
import os
import numpy as np

def recursive_get(data, dlg_list):

    if isinstance(data, list):
        dcc = {str(i) : s for i,s in enumerate(data)}
        data = dcc

    for k,v in data.items():
        if not (isinstance(v, dict) or isinstance(v, list)):
            continue
        elif "dlg" in v:
            dlg_list.append(data[k]['dlg'] + '\n')
        else:
            recursive_get(v, dlg_list)

flist = glob.glob('D:/GameUtil/UE4/FModel/Output/Exports/Uwo/Content/NonUFS/script/*.json')

for i, jsf in enumerate(flist):
    
    dlg_list = []

    fid = open(jsf, 'r', encoding='utf-8') 
    dlg_all = json.load(fid)
    fid.close()
    
    recursive_get(dlg_all, dlg_list)

    with open(os.path.join(os.path.dirname(jsf), 'dlg', os.path.basename(jsf) + '.txt') ,'w', encoding='utf-8') as fw:
        fw.writelines(dlg_list)
        fw.close()