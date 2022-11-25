import os
import glob
import json
import csv
import PIL.Image

from extract_util import uwo_readjson, PATH, PATH_SHIPSLOT, PATH_STATS, PATH_STATS_PASSIVE

def autocrop_shipparts_bakedsource() -> None:
    
    bakedsource = f"D:/UWO/unpack/221125/Shipparts_Texture2D_0.png"

    fp0 = PIL.Image.open(bakedsource, 'r')
    sp_all = uwo_readjson(os.path.join(PATH, PATH_SHIPSLOT))
    stat_all = uwo_readjson(os.path.join(PATH, PATH_STATS))
    pasv_all = uwo_readjson(os.path.join(PATH, PATH_STATS_PASSIVE))

    # "Name" -> "icon" in char_all

    sp_js = f"D:/UWO/unpack/image_crop_221125/Atlas/Icon_Item/Shipparts/**/*.json"

    flist = glob.glob(sp_js)

    data_all = []
    
    for i, fpath in enumerate(flist):

        if "Atlas_" in fpath:
            continue

        fid = open(fpath, 'r', encoding='utf-8') 
        jscontent = json.load(fid)
        if len(jscontent) > 1:
            data_all.append(jscontent[1])
        else:
            data_all.append(jscontent[0])
        fid.close()

    for j, data in enumerate(data_all):
        
        fcur = fp0

        try:
            icon_im = fcur.crop((data['Properties']['BakedSourceUV']['X'],
                                 data['Properties']['BakedSourceUV']['Y'],
                                 data['Properties']['BakedSourceUV']['X'] + data['Properties']['BakedSourceDimension']['X'],
                                 data['Properties']['BakedSourceUV']['Y'] + data['Properties']['BakedSourceDimension']['Y']))
        except:
            print(f"없는 아이템 (이미지 없음): {data['Name']}")
            continue
        
        for k, sp_data in sp_all.items():
            if "image" in sp_data:
                if sp_data['image'] == data['Name']:
                    if "name" in sp_data:
                        sp_dict = {'이름': f"{sp_data['name']}"}

                    if "stat" in sp_data:
                        ext_stats = sp_data['stat']

                        for i, stat in enumerate(ext_stats):
                            try:
                                sp_dict.update({stat_all[f"{stat['Type']}"]['desc']: stat['Val']})
                            except:
                                try:
                                    sp_dict.update({pasv_all[f"{stat['Type']}"]['desc']: stat['Val']})
                                except:
                                    continue
                
                    icon_im.save(f"./ext/{sp_dict['이름']}.png")

                    with open(f"./ext/{sp_dict['이름']}.csv", 'w', newline='', encoding='utf-8-sig') as out:
                        writer = csv.writer(out)
                        for k, v in sp_dict.items():
                            writer.writerow([k, v])
                    
        icon_im.close()

    fp0.close()

    return

if __name__ == "__main__":

    autocrop_shipparts_bakedsource()