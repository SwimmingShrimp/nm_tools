# coding=utf-8
import json
import os

def get_json_data(json_file):
    with open(json_file) as f:
        json_data = json.load(f)
        return json_data

src = '/home/lixialin/Downloads/json/night'
src1 = os.path.join(src,'fov30_night_591.json')
src2 = os.path.join(src,'night_fov30.json')
# src3 = os.path.join(src,'fov30_day_2750.json')
# src4 = os.path.join(src,'fov30_pic.json')
# src5 = os.path.join(src,'rainy_fov30.json')
dst = os.path.join(src,'night.json')

json_data = []
json_data1 = get_json_data(src1)
json_data2 = get_json_data(src2)
# json_data3 = get_json_data(src3)
# json_data4 = get_json_data(src4)
# json_data5 = get_json_data(src5)
# json_data = json_data1+json_data2 +json_data3 +json_data4 
json_data = json_data1+json_data2

with open(dst,'w') as f:
    json.dump(json_data, f, indent=4)


