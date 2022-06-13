import json
import os

json_src = 'C:/Users/李夏临/Desktop/3dDataset/3D激光数据外部标注'
json_dst = 'C:/Users/李夏临/Desktop/3dDataset/outlable_json_rename'
for  root, dirs, files in os.walk(json_src):
    for file_ in files:
        json_path = root + '/' + file_
        with open(json_path, 'r', encoding='utf8') as f:
            json_data = json.load(f)
            casename = json_data["baseUrl"].split('/')[-4]
            filename = json_data["baseUrl"].split('/')[-3]
            renamed_path = json_dst + '/' + casename
            if not os.path.exists(renamed_path):
                os.makedirs(renamed_path)
            command = 'cp {} {}/{}.json'.format(json_path,renamed_path,filename)
            print(command)
            os.system(command)
