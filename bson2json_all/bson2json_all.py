import glob
import json
import os
import bson

flist = glob.glob('D:/UWO/cmscurrent/*.bson', recursive=True)

for i, bsf in enumerate(flist):
    with open(bsf,'rb') as f:
        data = bson.decode_all(f.read())
        f.close()

    with open(bsf + '.json', "w", encoding='utf-8') as fw:
        json.dump(data, fw, indent=4, sort_keys=True, ensure_ascii=False)
        fw.close()
    
    os.remove(bsf)