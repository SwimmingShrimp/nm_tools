# coding = 'utf-8'
import os
import json

json_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/3d_outlable'
# json_files = os.listdir(json_src)
json_files =[]
for root,dirs, files in os.walk(json_src):
    for temp in files:
        if temp.endswith('.json'):
            file_path = root + '/' +temp
            json_files.append(file_path)
car = 0
truck =0
bus =0
ped = 0
tricycle =0
bicycle =0
motorcycle =0
for json_file in json_files:
    with open(json_file,'r',encoding='UTF-8') as f:
        json_data = json.load(f)
    items = json_data["frames"][0]["items"]
    for item in items:
        obstacle_type = (item["category"]).lower()
        print(obstacle_type)
        if obstacle_type=='truck':
            truck +=1
        if obstacle_type=='car':
            car +=1
        if obstacle_type=='bus':
            bus +=1
        if obstacle_type=='pedestrian':
            ped +=1
        if obstacle_type=='tricycle':
            tricycle +=1
        if obstacle_type=='bicycle':
            bicycle +=1
        if obstacle_type=='motorcycle':
            motorcycle +=1

print(car,bus,truck,ped,bicycle,motorcycle,tricycle)

        

    
