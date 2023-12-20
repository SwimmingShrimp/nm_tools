import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil

pic = '/home/lixialin/Videos/front_rp/gt_ori/front_far'
perce_json_path = '/home/lixialin/Videos/front_rp/perce_json/front_far'
dst = '/home/lixialin/Videos/front_rp/draw_perce/front_far'
os.makedirs(dst,exist_ok=True)

def draw_perce(pic_file,perce_json_data,dst):
    img = cv2.imread(pic_file)
    pic_name = os.path.basename(pic_file)
    if perce_json_data!=[]:
        for each in perce_json_data:
            top_cut = 180
            top_black = 0
            proportion_h = 3
            proportion_z = 3
            x = int(each["box2d"]["x"]*proportion_h)
            y = int(each["box2d"]["y"]*proportion_z + top_cut) 
            w = int(each["box2d"]["w"]*proportion_h)
            h = int(each["box2d"]["h"]*proportion_z)          
            x1 = x+w
            y1 = y+h
            cv2.rectangle(img, (x,y), (x1,y1),(255,0,255),3)
            # perce_type = each2["type"]
            # cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    print(os.path.join(dst,pic_name))
    cv2.imwrite(os.path.join(dst,pic_name),img)

for root,_,files in os.walk(pic):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        perce_json = file_.split('.')[0] + '.json'
        perce_json_data = utils.get_json_data(os.path.join(perce_json_path,perce_json))
        pic_path = os.path.join(root,file_)
        draw_perce(pic_path,perce_json_data,dst)

