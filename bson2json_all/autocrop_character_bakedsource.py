import os
import glob
import json
import csv
import PIL.Image

from extract_util import uwo_readjson, PATH, PATH_CHARACTER

def autocrop_character_bakedsource() -> None:
    
    bakedsource = f"D:/UWO/unpack/221221/Character_Texture2D_1.png"

    fp0 = PIL.Image.open(bakedsource, 'r')
    char_all = uwo_readjson(os.path.join(PATH, PATH_CHARACTER))

    # "Name" -> "icon" in char_all

    chars_js = f"D:/UWO/unpack/image_crop_221221/Atlas/Character/**/*.json"

    flist = glob.glob(chars_js)

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
        
        for k, char_data in char_all.items():
            if char_data['icon'] == data['Name']:
                if "firstName" in char_data and "familyName" in char_data:
                    char_dict = {'이름': f"{char_data['firstName']} {char_data['familyName']}"}
                elif "firstName" in char_data:
                    char_dict = {'이름': f"{char_data['firstName']}"}
                elif "familyName" in char_data:
                    char_dict = {'이름': f"{char_data['familyName']}"}

                if "desc" in char_data:
                    char_dict.update({'설명': char_data['desc']})

                if "age" in char_data:
                    char_dict.update({'나이': char_data['age']})

                if "breastSize" in char_data:
                    char_dict.update({'breastSize': char_data['breastSize']})
                
        icon_im.save(f"./ext/{char_dict['이름']}.png")
        icon_im.close()

        with open(f"./ext/{char_dict['이름']}.csv", 'w', newline='', encoding='utf-8-sig') as out:
            writer = csv.writer(out)
            for k, v in char_dict.items():
                writer.writerow([k, v])

    fp0.close()

    return

if __name__ == "__main__":

    autocrop_character_bakedsource()