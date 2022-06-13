import json
import os
import utils

enum_obstacle = {
    'car':1, 'truck':2, 'bus':3, 'pedestrian':4 ,'bicycle':5,'motorcycle':6 ,'tricycle':7}
err_json_path = 'D:/Projects/kpitool/2022-05-19-22-35-20/front_2d_precision_error/type_err_json'
perce_json_path = 'C:/Users/李夏临/Desktop/hengrun/day/json_perce'

for root,_,files in os.walk(err_json_path):
    for file_ in files:
        err_json_data = utils.get_json_data(os.path.join(root,file_))
        err_json_filename = os.path.basename(file_)
        perce_json_file = os.path.join(perce_json_path,err_json_filename)
        perce_json_data = utils.get_json_data(perce_json_file)
        for err_json_temp in err_json_data:
            err_h = err_json_temp["perce_box"]["obstacle_bbox.height"]
            lable_type = err_json_temp["lable_type"]
            if lable_type in ['bus','bicycle']:
                lable_type_value = enum_obstacle[lable_type]
                tacks_contxt = []
                for perce_json_temp in perce_json_data["tracks"]:
                    perce_json_temp_bak = perce_json_temp
                    perce_h = perce_json_temp["uv_bbox2d"]["obstacle_bbox.height"]
                    if err_h == perce_h:
                        perce_json_temp_bak["obstacle_type"] = lable_type_value
                    tacks_contxt.append(perce_json_temp_bak)
                perce_json_data["tracks"] = tacks_contxt
            # print(perce_json_data)
            with open(perce_json_file,'w') as f:
                utils.write_json_data(perce_json_file,perce_json_data)
            


            
