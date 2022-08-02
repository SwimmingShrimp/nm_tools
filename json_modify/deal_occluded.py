import os
import json
import sys
sys.path.append("..")
import utils

json_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/2D/label_json/day/day.json'
json_dst = '/home/lixialin/Pictures/day.json'

json_data = utils.get_json_data(json_src)
for temp in json_data:
    for temp1 in temp["task_vehicle"]:
        if 'occluded' not in temp1["tags"]:
            temp1["tags"]["occluded"]="0"
utils.write_json_data(json_dst,json_data)

