import json
import os

def get_json_data(json_file):
    with open(json_file) as f:
        json_data = json.load(f)
        return json_data

def write_json_data(json_file,str_content):
    with open(json_file,'w')  as f:
        json.dump(str_content,f,indent=4)

json_src = '/data1/NMtest/HengRun/front_2d/json_gt/night/night.json'
json_path_src = '/data1/NMtest/HengRun/front_2d/json_gt/night'


enum_obstacle= {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',7: 'tricycle',9:'wheel'}


json_data = get_json_data(json_src)
json_dst_data = []

for json_temp in json_data:    
    item_content = {}
    filename= json_temp["filename"]
    task_attention_area = json_temp["task_attention_area"]
    json_result = { 
    "imgsize_wh": [
        1920,
        1080
    ],
    "filename" : filename,
    "task_attention_area" : task_attention_area,
    "items": None
    }
    if not json_temp["task_vehicle"]:
        continue
    new_task_vehicle =[]
    for temp in json_temp["task_vehicle"]:
        if temp==None:
            continue
        obstacle_class = temp["tags"]["class"]
        h = round(temp["tags"]["height"],3)
        w = round(temp["tags"]["width"],3)
        x = round(temp["tags"]["x"],3)
        y = round(temp["tags"]["y"],3)
        item_temp = {}
        item_temp["class"] = obstacle_class
        item_temp["occluded"] = temp["tags"]["occluded"]
        item_temp["box_2d"] = [x,y,w,h]
        item_temp["box_3d"] = {
                "center":[
                    -1000,
                    -1000,
                    -1000
                ],
                "dimension": [
                    -1,
                    -1,
                    -1
                ],
                "heading_yaw": -10
                }
        item_temp["id"] = -1
        new_task_vehicle.append(item_temp)
    json_result["items"] = new_task_vehicle
    json_dst_data.append(json_result)
json_dst_src = json_path_src.replace('HengRun','Hirain_20220528')
os.makedirs(json_dst_src,exist_ok=True)
json_dst_file = json_src.replace('HengRun','Hirain_20220528')
write_json_data(json_dst_file,json_dst_data)



