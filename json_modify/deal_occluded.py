import os
import json
import sys
sys.path.append("..")
import utils

json_src = '/home/NULLMAX/lixialin/视频/day.json'
json_dst = '/home/NULLMAX/lixialin/视频/day1.json'

json_data = utils.get_json_data(json_src)
for temp in json_data:
    for temp1 in temp["task_vehicle"]:
        if 'occluded' not in temp1["tags"]:
            temp1["tags"]["occluded"]="0"
utils.write_json_data(json_dst,json_data)

