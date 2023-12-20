import os
import sys
sys.path.append('..')
import utils
import imagesize
import cv2

with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/relation.txt','r') as f1:
    for line in f1.readlines():
        imgoldpath,imgnewname,imgsize = line.strip().split('|')
        old_json = imgoldpath.replace('IMAGE','NM_LABEL').split('.')[0] + '.json'
        new_json_name = imgnewname.split('.')[0] + '.json'
        new_json = os.path.join('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/chery_json_1920x1280',new_json_name)
        if imgsize=='3840x2160':
            json_data = utils.get_json_data(old_json)
            for temp in json_data["traffic_sign"]:
                temp["xywh"][0] = temp["xywh"][0]/2 
                temp['xywh'][1] = temp['xywh'][1]/2 + 100
                temp['xywh'][2] = temp['xywh'][2]/2 
                temp['xywh'][3] = temp['xywh'][3]/2 
            utils.write_json_data(new_json,json_data)
        elif imgsize=='1920x1080':
            json_data = utils.get_json_data(old_json)
            for temp in json_data["traffic_sign"]:
                temp['xywh'][0] = temp['xywh'][0] 
                temp['xywh'][1] = temp['xywh'][1] + 100
                temp['xywh'][2] = temp['xywh'][2] 
                temp['xywh'][3] = temp['xywh'][3] 
            utils.write_json_data(new_json,json_data)
        else:
            command = 'cp {} {}'.format(old_json,new_json)
            os.system(command)