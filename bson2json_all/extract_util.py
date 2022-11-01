import glob
import json
import os

PATH_ITEM = "Item_s*.json"
PATH_STATS = "StatOperator_s*.json"
PATH_EQUIP = "CEquip_s*.json"
PATH_SHIP = "Ship_s*.json"
PATH_SHIPBP = "ShipBlueprint_s*.json"

PATH = f"D:\\UWO\\cmscurrent\\"

def uwo_readjson(jsonpath:list) -> dict:
    flist = glob.glob(jsonpath)
    for i, fpath in enumerate(flist):
        fid = open(fpath, 'r', encoding='utf-8') 
        data = json.load(fid)[0]
        fid.close()

    return data

def extract_shiptier(tier:int) -> None:
    
    # Blueprint
    matched_bp = []
    
    shipbp_all = uwo_readjson(os.path.join(PATH, PATH_SHIPBP))

    for j, bplist in enumerate(shipbp_all):
        for k, v in shipbp_all[bplist].items():
            if k == 'tier' and v == tier:
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
        result_dict = {
            '이름': '',
            '설명': '',
            '티어': '',
            '최소선원수': '',
            '최대선원수': '',
            '최대내구도': '',
            '적재량': '',
            '조력': '',
            '내파': '',
            '세로돛': '',
            '가로돛': '',
            '포격위력': '',
            '백병위력': '',
            '충파위력': '',
            '추가포격방어력': '',
            '추가백병방어력': '',
            '추가충파방어력': '',
            '추가수리회복량': '',
            '추가의술회복량': '',
            }

        result.append(result_dict)

    pass

if __name__ == "__main__":

    extract_shiptier(14)