import os
import json
import sys
sys.path.append("..")
import utils

txt_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/hengrun/relation.txt'
json_src = '/home/NULLMAX/lixialin/视频/new_json_gt/day.json'
json_new_src = '/home/NULLMAX/lixialin/视频/new_json_gt/day_new.json'
json_data = utils.get_json_data(json_src)
json_new = []
with open(txt_src,'r') as f:
    while True:
        line_str = f.readline()
        file_old = (((line_str).split('|')[0]).split('/'))[-1]
        file_new = ((line_str).split('|')[-1])[:-1]
        print(file_old,file_new)
        for temp in json_data:
            context = temp
            filename = temp["filename"]
            if filename==file_old:
                context["filename"]=file_new
                json_new.append(context)
                break
        if not line_str:
            break
   

utils.write_json_data(json_new_src,json_new)
