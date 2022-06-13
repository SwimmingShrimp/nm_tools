import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
import json
import copy

json_src = 'C:/Users/李夏临/Desktop/test/day.json'
x = 'C:/Users/李夏临/Desktop/test/day_filter.json'

with open(json_src,'r') as f:
    json_data = json.load(f)

temp4 = []
for temp  in json_data:
    temp_copy = copy.deepcopy(temp)
    temp3 =[]
    for temp1 in temp["task_vehicle"]:
        temp1_copy = copy.deepcopy(temp1)
        if temp1["tags"]["class"]=='car':
            if temp1["tags"]["width"] <=35 and temp1["tags"]["height"] <=30:
                temp1_copy["tags"]["occluded"]=1
        if temp1["tags"]["class"]=='truck':
            if temp1["tags"]["width"] <=35 and temp1["tags"]["height"] <=30:
                temp1_copy["tags"]["occluded"]=1
        if temp1["tags"]["class"]=='bus':
            if temp1["tags"]["width"] <=35 and temp1["tags"]["height"] <=30:
                temp1_copy["tags"]["occluded"]=1
        if temp1["tags"]["class"]=='pedestrian':
            if temp1["tags"]["height"] <=40 and temp1["tags"]["width"] <=10:
                temp1_copy["tags"]["occluded"]=1
        if temp1["tags"]["class"]=='motorcycle':
            if temp1["tags"]["height"] <=45 and temp1["tags"]["width"] <=30:
                temp1_copy["tags"]["occluded"]=1
        if temp1["tags"]["class"]=='bicycle':
            if temp1["tags"]["height"] <=45 and temp1["tags"]["width"] <=30:
                temp1_copy["tags"]["occluded"]=1
        temp3.append(temp1_copy)
    temp_copy["task_vehicle"] = temp3
    temp4.append(temp_copy)
with open(x,'w') as f1:
    json.dump(temp4,f1,indent=4)

        

