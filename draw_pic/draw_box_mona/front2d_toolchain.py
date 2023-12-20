import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil

def perce_draw_box(perce_json,pic_file,dst):
    with open(perce_json,'r') as f2: 
        perce_json_data = json.load(f2)
        img = cv2.imread(pic_file)
        pic_name = os.path.basename(pic_file)
        top_cut = 40
        top_black = 0
        proportion_h = 3
        proportion_z = 3
        for each in perce_json_data:
            x = int(each["box2d"]["x"]*proportion_h)
            y = int(each["box2d"]["y"]*proportion_z) + top_cut
            w = int(each["box2d"]["w"]*proportion_h)
            h = int(each["box2d"]["h"]*proportion_z)
            x1 = x+w
            y1 = y+h
            cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
            if int(each["obstacle_type"])<10:
                perce_type = config.front_config["enum_obstacle3"][int(each["obstacle_type"])]
                cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
        print(os.path.join(dst,pic_name))
        cv2.imwrite(os.path.join(dst,pic_name),img)

dst ='/home/lixialin/Videos/pic'
if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(dst,exist_ok=True)

json_src_perce = '/home/lixialin/Downloads/perce_json/front_near'
pic_src = '/home/lixialin/Downloads/image/front_near'
for root,_,files in os.walk(json_src_perce):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        perce_json = os.path.join(root,file_)
        pic_file = os.path.join(pic_src,str(int(file_.split('.')[0]))+'.jpg')
        perce_draw_box(perce_json,pic_file,dst)






