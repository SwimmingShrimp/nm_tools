import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil

pic = '/home/lixialin/Videos/tl_rp/tl_145054/img_ori_gt/front_near'
perce_json_path = '/home/lixialin/Videos/tl_rp/tl_145054/perce_json/front_near'
dst = '/home/lixialin/Videos/tl_rp/tl_145054/img/front_near'
gt_json_path = '/home/lixialin/Videos/tl_rp/tl_145054/gt_json_1'
os.makedirs(dst,exist_ok=True)

def draw_perce(pic_file,perce_json_data,dst):
    img = cv2.imread(pic_file)
    pic_name = os.path.basename(pic_file)
    if perce_json_data!=[]:
        for each in perce_json_data:
            top_cut = 40
            top_black = 0
            proportion_h = 3
            proportion_z = 3
            x = int(each["box2d"]["x"]*proportion_h)
            y = int(each["box2d"]["y"]*proportion_z + top_cut) 
            w = int(each["box2d"]["w"]*proportion_h)
            h = int(each["box2d"]["h"]*proportion_z)          
            x1 = x+w
            y1 = y+h
            cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
            perce_type = each["tl_detection"].split("_")
            perce_type_all = ''
            for temp in perce_type:
                if perce_type_all == '':
                    perce_type_all = config.front_config["enum_tl_value_2_direct"][int(temp)]
                else:
                    perce_type_all = perce_type_all + '_' + config.front_config["enum_tl_value_2_direct"][int(temp)]
            print(perce_type_all)
            cv2.putText(img,perce_type_all,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.imwrite(os.path.join(dst,pic_name),img)


def draw_gt(pic_file,gt_file,dst):
    img = cv2.imread(pic_file)
    pic_name = os.path.basename(pic_file)
    if gt_file!={} and gt_file["obstacle_tl"]!=[]:
        for each in gt_file["obstacle_tl"]:
            for each2 in each['2d']:
                if int(each2["cameraId"])==1:            
                    x = int(each2["x"])
                    y = int(each2["y"]) 
                    w = int(each2["width"])
                    h = int(each2["height"])
                    x1 = x+w
                    y1 = y+h
                    cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
                    perce_type = each2["direction"]["forward"] + '_' +each2["direction"]["left"] + '_' +each2["direction"]["right"] + '_' +each2["direction"]["uturn"]
                    cv2.putText(img,perce_type,(x1+20,y1-20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),2)
    print(os.path.join(dst,pic_name))
    cv2.imwrite(os.path.join(dst,pic_name),img)

for root,_,files in os.walk(pic):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        gt_json = file_.split('.')[0] + '.json'
        gt_json_data = utils.get_json_data(os.path.join(gt_json_path,gt_json))
        pic_path = os.path.join(root,file_)
        draw_gt(pic_path,gt_json_data,dst)

# for root,_,files in os.walk(dst):
#     files = sorted(files,key=lambda x:int(x.split('.')[0]))
#     for file_ in files:
#         perce_json = file_.split('.')[0] + '.json'
#         perce_json_data = utils.get_json_data(os.path.join(perce_json_path,perce_json))
#         pic_path = os.path.join(root,file_)
#         draw_perce(pic_path,perce_json_data,dst)