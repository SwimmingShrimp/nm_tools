import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil

pic = '/home/lixialin/Videos/tsr_dist/gt_pic_ori/front_far'
perce_json_path = '/home/lixialin/Videos/tsr_dist/perce_json'
dst = '/home/lixialin/Videos/tsr_dist/draw_perce/front_far'
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
            x = int(each["box_2d"]["x"]*proportion_h)
            y = int(each["box_2d"]["y"]*proportion_z + top_cut) 
            w = int(each["box_2d"]["w"]*proportion_h)
            h = int(each["box_2d"]["h"]*proportion_z)          
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
            y = int(each["box2d"]["y"]*proportion_z + top_cut) 
            w = int(each["box2d"]["w"]*proportion_h)
            h = int(each["box2d"]["h"]*proportion_z)
            x1 = x+w
            y1 = y+h
            cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
            # perce_type = config.front_config["enum_obstacle3"][int(each["obstacle_type"])]
            # cv2.putText(img,'',(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
        print(os.path.join(dst,pic_name))
        cv2.imwrite(os.path.join(dst,pic_name),img)

def lable_draw_box(lable_json,pic_file,dst):
    img = cv2.imread(pic_file)
    with open(lable_json,'r') as f2 :
        lable_json_data = json.load(f2)
        if  lable_json_data['task_vehicle']:
            for each in lable_json_data['task_vehicle']:
                x = int(each["tags"]["x"])
                y = int(each["tags"]["y"])
                w = int(each["tags"]["width"])
                h = int(each["tags"]["height"])
                lable_type = each["obstacle_type"]
                cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),3)
                cv2.putText(img,lable_type,(x+w-20,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.imwrite(pic_file,img)

dst ='/home/lixialin/Videos/tl/tl_145054/img_ori_perce/front_near'
if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(dst,exist_ok=True)
json_src_perce = '/home/lixialin/Videos/tl/tl_145054/perce_json/front_near'
pic_src = '/home/lixialin/Videos/tl/tl_145054/img_ori/front_near'
for root,_,files in os.walk(json_src_perce):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        perce_json = os.path.join(root,file_)
        pic_file = os.path.join(pic_src,str(int(file_.split('.')[0]))+'.jpg')
        perce_draw_box(perce_json,pic_file,dst)






