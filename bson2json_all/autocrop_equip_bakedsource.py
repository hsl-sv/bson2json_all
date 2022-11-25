import os
import glob
import json
import csv
import PIL.Image

from extract_util import uwo_readjson, PATH, PATH_STATS_PASSIVE, PATH_STATS, PATH_EQUIP

def autocrop_equip_bakedsource() -> None:

    tmp_equip0 = f"D:/UWO/unpack/221125/Equip_Texture2D_0.png"
    tmp_equip1 = f"D:/UWO/unpack/221125/Equip_Texture2D_1.png"
    tmp_equip2 = f"D:/UWO/unpack/221125/Equip_Texture2D_2.png"

    fp0 = PIL.Image.open(tmp_equip0, 'r')
    fp1 = PIL.Image.open(tmp_equip1, 'r')
    fp2 = PIL.Image.open(tmp_equip2, 'r')
    equip_all = uwo_readjson(os.path.join(PATH, PATH_EQUIP))
    stat_all = uwo_readjson(os.path.join(PATH, PATH_STATS))
    pasv_all = uwo_readjson(os.path.join(PATH, PATH_STATS_PASSIVE))

    # Icon_CEquip_<itemID>_<C/M/F>_Sprite.json
    # <itemID> is key of PATH_EQUIP
    # desc, specialStat, statEffect
    tmp_Equips_js = f"D:/UWO/unpack/image_crop_221125/Atlas/Icon_Item/Equip/**/*.json"

    flist = glob.glob(tmp_Equips_js)

    data_all = []
    
    for i, fpath in enumerate(flist):

        if "Atlas_" in fpath:
            continue

        fid = open(fpath, 'r', encoding='utf-8') 
        data_all.append(json.load(fid)[1])
        fid.close()

    for j, data in enumerate(data_all):

        imgswitch = data['Properties']['BakedSourceTexture']['ObjectName'].split(':')[1]

        fcur = fp0
        if imgswitch == "Texture2D_1":
            fcur = fp1
        elif imgswitch == "Texture2D_2":
            fcur = fp2

        icon_im = fcur.crop((data['Properties']['BakedSourceUV']['X'],
                             data['Properties']['BakedSourceUV']['Y'],
                             data['Properties']['BakedSourceUV']['X'] + data['Properties']['BakedSourceDimension']['X'],
                             data['Properties']['BakedSourceUV']['Y'] + data['Properties']['BakedSourceDimension']['Y']))
        
        equip_id = data['Name'].split('_')[2]

        try:
            equip_target = equip_all[equip_id]
        except:
            print(f"없는 장비: {equip_id}")
            ftmp = open(f"./ext/{equip_id}_없는장비.csv", 'w', newline='', encoding='utf-8-sig')
            ftmp.close()
            icon_im.save(f"./ext/{equip_id}.png")
            icon_im.close()
            continue

        nostat = False

        if "statEffect" in equip_target:
            ext_stats = equip_target['statEffect']
        else:
            nostat = True
            
        equip_dict = {
            '이름': equip_target['name'],
            }

        if "desc" in equip_target:
            equip_dict.update({'설명': equip_target['desc']})

        if not nostat:
            for i, stat in enumerate(ext_stats):
                try:
                    equip_dict.update({stat_all[f"{stat['Id']}"]['desc']: stat['Value']})
                except:
                    try:
                        equip_dict.update({pasv_all[f"{stat['Id']}"]['desc']: stat['Value']})
                    except:
                        continue

        icon_im.save(f"./ext/{equip_id}.png")
        icon_im.close()

        with open(f"./ext/{equip_id}.csv", 'w', newline='', encoding='utf-8-sig') as out:
            writer = csv.writer(out)
            for k, v in equip_dict.items():
                writer.writerow([k, v])

    fp0.close()
    fp1.close()
    fp2.close()

    return

if __name__ == "__main__":

    autocrop_equip_bakedsource()