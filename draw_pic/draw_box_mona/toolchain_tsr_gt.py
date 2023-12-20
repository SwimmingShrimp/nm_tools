import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil
import numpy as np

pic = '/home/lixialin/Videos/tsr_dist/gt_pic_ori/front_far'
gt_json_path = '/home/lixialin/Videos/tsr_dist/gt_json'
dst = '/home/lixialin/Videos/tsr_dist/draw_gt/front_far'
os.makedirs(dst,exist_ok=True)

def draw_gt(pic_file,gt_file,dst):
    img = cv2.imread(pic_file)
    pic_name = os.path.basename(pic_file)
    if gt_file!={} and gt_file["obstacle_tsr"]!=[]:
        for each in gt_file["obstacle_tsr"]:
            for each2 in each['2d']:
                if int(each2["cameraId"])==0:            
                    x = int(each2["x"])
                    y = int(each2["y"]) 
                    w = int(each2["width"])
                    h = int(each2["height"])
                    x1 = x+w
                    y1 = y+h
                    cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
                    # perce_type = each2["type"]
                    # cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    print(os.path.join(dst,pic_name))
    cv2.imwrite(os.path.join(dst,pic_name),img)

for root,_,files in os.walk(pic):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        gt_json = file_.split('.')[0] + '.json'
        gt_json_data = utils.get_json_data(os.path.join(gt_json_path,gt_json))
        pic_path = os.path.join(root,file_)
        draw_gt(pic_path,gt_json_data,dst)




