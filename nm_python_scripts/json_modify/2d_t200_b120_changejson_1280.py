'''
原图1920X1280
'''

import os
import json
from pickletools import TAKEN_FROM_ARGUMENT1

src = 'C:/Users/李夏临/Desktop/test/day_filter.json'
dst = 'C:/Users/李夏临/Desktop/test/day_filter_modify.json'

with open(src,'r') as f:
    json_data = json.load(f)

new_json = []
for temp in json_data:
    temp1 = temp
    task_v = []
    for tag in temp["task_vehicle"]:
        tag1 = tag
        y = tag["tags"]["y"]
        h = tag["tags"]["height"]
        if y+h<200:
            tag1 =[]
        if y>1160:
            tag1 =[]
        if y<200 and 200<y+h<1160:
            tag1["tags"]["y"]= 0
            tag1["tags"]["height"] = y+h-200  
        if 200<y<1160 and 200<y+h<1160:
            tag1["tags"]["y"]= y-200
        if 200<y<1160 and y+h>1160:
            tag1["tags"]["y"]=y-200
            tag1["tags"]["height"] = 1160-y
        if y<200 and y+h>1160:
            tag1["tags"]["y"]=0
            tag1["tags"]["height"] = 960        
        task_v.append(tag1)
    temp1["task_vehicle"] = task_v
    new_json.append(temp1)

with open(dst,'w') as f1:   
    json.dump(new_json,f1,indent=4)
