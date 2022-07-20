from distutils import command
from operator import ne
import sys
sys.path.append("..")
import utils
import os


txtfile = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/relation.txt'
dict1 = {}
with open(txtfile,'r') as f:
    for line in f.readlines():
        keyx = ((line.split("|")[0]).split("/")[-1]).split('.')[0]
        valuex = ((line.split("|")[-1]).split('.')[0]).split('_')[-1]
        dict1[keyx] = valuex

'''
修改高精地图数据
'''
HDmap = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/qirui_map_shanghai.json'
dst = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/new/HDmap_shanghai.json'
# json_data = utils.get_json_data(HDmap)
# newHDmap_json = {
#     "header": {
#         "coordinate": "CUSTOM",
#         "major_version": 0,
#         "minor_version": 1,
#         "region": "../map/qirui_shanghai_demo",
#         "zone": 51
#     },
#     "lane_markings": [],
#     "road_objects": []}

# marking = []
# for temp in json_data["lane_markings"]:
#     if str(temp["id"]) not in dict1.keys():
#         continue
#     else:
#         id_value = temp["id"]
#         temp["id"] = int(dict1[str(id_value)])
#         marking.append(temp)
# newHDmap_json["lane_markings"] = marking

# road_objects = []
# for temp in json_data["road_objects"]:
#     if str(temp["id"]) not in dict1.keys():
#         continue
#     else:
#         id_value = temp["id"]
#         temp["id"] = int(dict1[str(id_value)])
#         road_objects.append(temp)
# newHDmap_json["road_objects"] = road_objects

# utils.write_json_data(dst,newHDmap_json)

'''
修改时间戳数据
'''
timestampfile = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/update_timestamp_vc1.log'
new_timestampfile = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/new/timestamp_vc1.log'
# with open(timestampfile,'r') as f2:
#     with open(new_timestampfile,'a+') as f3:
#         for line in f2.readlines():
#             line = line.strip()            
#             frame_id = line.split(' ')[-1]            
#             if frame_id in dict1.keys():
#                 print(line)
#                 print(type(frame_id),frame_id)
#                 comment = line.rsplit(' ',1)[0] + ' ' + dict1[frame_id] + '\n'
#                 print(comment)
#                 f3.write(comment)
'''
修改车身数据
'''
vehicle = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/update_vehicle.log'
new_vehicle = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/new/vehicle.log'
# with open(vehicle,'r') as f4:
#     with open(new_vehicle,'a+') as f5:
#         for line in f4.readlines():
#             line = line.strip()            
#             frame_id = line.split(' ')[-1]            
#             if frame_id in dict1.keys():
#                 comment = line.rsplit(' ',1)[0] + ' ' + dict1[frame_id] + '\n'
#                 print(line)
#                 print(comment)
                # f5.write(comment)
'''
修改novatel的数据
'''        
novatel = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/novatel.txt'
new_novatel = '/media/lixialin/lxl/1_dataset/chery_HDmap_lane/HDmap_data/new/novatel.txt'
with open(novatel,'r') as f6:
    with open(new_novatel,'a+') as f7:
        for line in f6.readlines():
            line = line.strip()            
            frame_id = line.split(' ')[0]
            if frame_id in dict1.keys():
                comment =  dict1[frame_id] + ' ' +  line.split(' ',1)[-1] +  '\n'
                print(line)
                print(comment)
                f7.write(comment)
