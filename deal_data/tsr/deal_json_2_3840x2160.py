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
        new_json = os.path.join('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/lable_json',new_json_name)
        if imgsize!='3840x2160':
            json_data = utils.get_json_data(old_json)
            new_json_data = json_data
            for temp in json_data["traffic_sign"]:
                # temp1 = temp
                temp['xywh'][0] = temp['xywh'][0]*2
                temp['xywh'][1] = temp['xywh'][1]*2
                temp['xywh'][2] = temp['xywh'][2]*2
                temp['xywh'][3] = temp['xywh'][3]*2
            utils.write_json_data(new_json,new_json_data)
        else:
            command = 'cp {} {}'.format(old_json,new_json)
            os.system(command)