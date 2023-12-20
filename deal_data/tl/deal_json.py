import os
import sys
sys.path.append('..')
import utils
import cv2

with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/traffic_light_benchmark/relation.txt','r') as f1:
    for line in f1.readlines():
        imgoldpath,imgnewname,imgsize = line.strip().split('|')
        old_json = imgoldpath.replace('IMAGE','NM_LABEL').split('.')[0] + '.json'
        new_json_name = imgnewname.split('.')[0] + '.json'
        new_json = os.path.join('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/lable_json',new_json_name)
        command = 'cp {} {}'.format(old_json,new_json)
        os.system(command)