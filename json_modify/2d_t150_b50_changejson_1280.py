'''
原图1920X1280
'''

import os
import json
from pickletools import TAKEN_FROM_ARGUMENT1

src = 'C:/Users/李夏临/Desktop/json/old_json/day/day.json'
dst = 'C:/Users/李夏临/Desktop/json/new_json/day/day.json'

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
        if y<150 and y+h<150:
            tag1 =[]
        if y>1230:
            tag1 =[]
        if y<150 and 150<y+h<1230:
            tag1["tags"]["y"]= 0
            tag1["tags"]["height"] = y+h-150  
        if 150<y<1230 and 150<y+h<1230:
            tag1["tags"]["y"]= y-150
        if 150<y<1230 and y+h>1230:
            tag1["tags"]["y"]=y-150
            tag1["tags"]["height"] = 1080-y
        if y<150 and y+h>1230:
            tag1["tags"]["y"]=0
            tag1["tags"]["height"] = 1080

        
        task_v.append(tag1)
    temp1["task_vehicle"] = task_v
    new_json.append(temp1)

# temp3 = []
# for temp1 in new_json:
#     temp2 = []
#     list_x = []
#     list_y = []
#     list_n_x = []
#     list_n_y = []
#     list_x = temp1["task_attention_area"][0]["tags"]["xn"]
#     list_y = temp1["task_attention_area"][0]["tags"]["yn"]
#     list_x_1 = list_x.split(';')
#     list_y_1 = list_y.split(';')
#     for i in range(len(list_y_1)):
#         if float(list_y_1[i])>1080:
#             list_n_x.append(list_x_1[i])
#             y_value = '960'
#             list_n_y.append(y_value)
#         if 1080>float(list_y_1[i])>120:
#             list_n_x.append(list_x_1[i])
#             y_value = float(list_y_1[i])-120
#             list_n_y.append(str('%.2f' % y_value))
#         if float(list_y_1[i])<120:
#             list_n_x.append(list_x_1[i])
#             y_value = '0'
#             list_n_y.append(y_value)
        
#     temp2 = temp1
#     temp2["task_attention_area"][0]["tags"]["xn"] = ';'.join(list_n_x)
#     temp2["task_attention_area"][0]["tags"]["yn"] = ';'.join(list_n_y)
#     temp3.append(temp2)
        
with open(dst,'w') as f1:   
    json.dump(new_json,f1,indent=4)
