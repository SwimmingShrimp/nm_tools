import json
import os

def get_json_data(json_file):
    with open(json_file) as f:
        json_data = json.load(f)
        return json_data

def write_json_data(json_file,str_content):
    with open(json_file,'w')  as f:
        json.dump(str_content,f,indent=4)

json_src = '/data1/NMtest/HengRun/front_2d/json_perce'


enum_obstacle= {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',7: 'tricycle'}

for root,_,files in os.walk(json_src):
    for file_ in files:
        json_file_src = os.path.join(root,file_)
        json_data = get_json_data(json_src)
        json_result = { 
            "imgsize_wh": [
                640,
                384
            ],
            "items": None
            }
        item_content = []

        for temp in json_data["tracks"]:
            obstacle_class_value = temp["obstacle_type"]
            obstacle_class = enum_obstacle[obstacle_class_value]
            h = round(temp["uv_bbox2d"]["obstacle_bbox.height"],3)
            w = round(temp["uv_bbox2d"]["obstacle_bbox.width"],3)
            x = round(temp["uv_bbox2d"]["obstacle_bbox.x"],3)
            y = round(temp["uv_bbox2d"]["obstacle_bbox.y"],3)
            item_temp = {}
            item_temp["class"] = obstacle_class
            item_temp["box_2d"] = [x,y,w,h]
            item_temp["box_3d"] = {
                    "center":[
                        -1,
                        -1,
                        -1
                    ],
                    "dimension": [
                        -1,
                        -1,
                        -1
                    ],
                    "heading_yaw": -1
                    }
            item_temp["id"] = -1
            item_content.append(item_temp)
        json_result["items"] = item_content
        json_dst = json_file_src.replace('HengRun','Hirain_20220528')
        os.makedirs(json_dst,exist_ok=True)
        write_json_data(json_dst,json_result)



