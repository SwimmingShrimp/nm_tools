import os
import json
import sys
sys.path.append("..")
import utils

json_src = '/home/lixialin/Downloads/json/night/night.json'
json_dst = '/home/lixialin/Downloads/json/night/night1.json'

json_data = utils.get_json_data(json_src)
for temp in json_data:
    for temp1 in temp["task_vehicle"]:
        if 'occluded' not in temp1["tags"]:
            temp1["tags"]["occluded"]="0"
utils.write_json_data(json_dst,json_data)

