﻿import glob
import json
import os
import csv
import math

PATH_ITEM = "Item_s*.json"
PATH_STATS = "StatOperator_s*.json"
PATH_STATS_PASSIVE = "WorldPassiveEffect_s*.json"
PATH_STATS_SPECIAL = "SpecialStat_s*.json"
PATH_EQUIP = "CEquip_s*.json"
PATH_SHIP = "Ship_s*.json"
PATH_SHIPBP = "ShipBlueprint_s*.json"
PATH_SHIPSLOT = "ShipSlot_s*.json" # ShipParts
PATH_CHARACTER = "Character_s*.json"

PATH = f"D:\\UWO\\cmscurrent\\"

def uwo_readjson(jsonpath:list) -> dict:
    flist = glob.glob(jsonpath)
    data_all = {}
    for i, fpath in enumerate(flist):
        fid = open(fpath, 'r', encoding='utf-8') 
        data_all.update(json.load(fid)[0])
        fid.close()

    return data_all

def extract_shiptier(tier:int) -> list:
    
    # Blueprint
    matched_bp = []
    
    shipbp_all = uwo_readjson(os.path.join(PATH, PATH_SHIPBP))

    for j, bplist in enumerate(shipbp_all):
        for k, v in shipbp_all[bplist].items():
            if k == 'tier' and v == tier:
                #print(shipbp_all[bplist])
                matched_bp.append(shipbp_all[bplist])

    # Item
    item_all = uwo_readjson(os.path.join(PATH, PATH_ITEM))

    # Ship
    ship_all = uwo_readjson(os.path.join(PATH, PATH_SHIP))

    # StatOperator    
    stat_all = uwo_readjson(os.path.join(PATH, PATH_STATS))

    # Rebuild
    result = []

    for i, blueprint in enumerate(matched_bp):
        ext_id = blueprint['id']
        ext_shipid = blueprint['shipId']
        ext_stats = blueprint['stat']

        if 'materialItem' in blueprint:
            matav = True
            ext_material = blueprint['materialItem']
        else:
            matav = False
        
        try:
            result_dict = {
                '이름': ship_all[f"{ext_shipid}"]["name"],
                '설명': ship_all[f"{ext_shipid}"]["desc"],
                '티어': blueprint['tier'],
                }

            for j, stat in enumerate(ext_stats):
                result_dict.update({stat_all[f"{stat['Type']}"]['desc']: f"{math.ceil(stat['MinRate'] / 1000 * stat['Val'])}-{stat['Val']}"})

            if matav:
                for k, mat in enumerate(ext_material):
                    result_dict.update({item_all[f"{mat['Id']}"]['name']: mat['Val']})

            result.append(result_dict)
        except:
            print(f"잘못된 내용: ShipID: {ext_shipid}")
            pass

    return result

def extract_shiptier_batch(cursor):
    ext_test = extract_shiptier(cursor)

    for i in range(len(ext_test)):
        with open(f"./T{ext_test[i]['티어']}_{ext_test[i]['이름']}.csv", 'w', newline='', encoding='utf-8-sig') as out:
            writer = csv.writer(out)
            for k, v in ext_test[i].items():
                writer.writerow([k, v])

if __name__ == "__main__":

    for aa in range(99):
        
        extract_shiptier_batch(aa)