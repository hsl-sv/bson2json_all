import os
import glob
import json
import csv
import PIL.Image

from extract_util import uwo_readjson, PATH, PATH_ITEM

def autocrop_item_bakedsource() -> None:
    
    bakedsource = f"D:/UWO/unpack/221125/Item_Texture2D_1.png"

    fp0 = PIL.Image.open(bakedsource, 'r')
    item_all = uwo_readjson(os.path.join(PATH, PATH_ITEM))

    # Icon_Item_<itemID>_Sprite.json
    # <itemID> is key of PATH_ITEM

    items_js = f"D:/UWO/unpack/image_crop_221125/Atlas/Icon_Item/Item/**/*.json"

    flist = glob.glob(items_js)

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
        
        item_id = data['Name'].split('_')[2]

        try:
            equip_target = item_all[item_id]
        except:
            print(f"없는 아이템: {item_id}")
            ftmp = open(f"./ext/{item_id}_없는아이템.csv", 'w', newline='', encoding='utf-8-sig')
            ftmp.close()
            icon_im.save(f"./ext/{item_id}.png")
            icon_im.close()
            continue
        
        equip_dict = {
            '이름': equip_target['name'],
            }

        try:
            equip_dict.update({'설명': equip_target['desc']})
        except:
            pass
        

        icon_im.save(f"./ext/{item_id}.png")
        icon_im.close()

        with open(f"./ext/{item_id}.csv", 'w', newline='', encoding='utf-8-sig') as out:
            writer = csv.writer(out)
            for k, v in equip_dict.items():
                writer.writerow([k, v])

    fp0.close()

    return

if __name__ == "__main__":

    autocrop_item_bakedsource()