import os
import cv2
import json
import sys
sys.path.append('../..')
import config
import shutil

def perce_draw_box(perce_json,pic_file,dst):
    with open(perce_json,'r') as f2: 
        perce_json_data = json.load(f2)
        img = cv2.imread(pic_file)
        pic_name = os.path.basename(pic_file)
        top_cut = 0
        top_black = 0
        proportion_h = 1
        proportion_z = 1
        if  perce_json_data[0]['front_near']["detect_result"]:
            for each in perce_json_data[0]["front_near"]["detect_result"]:
                x = int(each[2]*proportion_h)
                y = int(each[3]*proportion_h) + top_cut -top_black
                x1 = int(each[4]*proportion_h)
                y1 = int(each[5]*proportion_h) + top_cut -top_black
                cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),1)
                perce_type = config.front_config["enum_obstacle1"][int(each[0])]
                cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
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
                lable_type = each["tags"]["class"]
                cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),3)
                cv2.putText(img,lable_type,(x+w-20,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.imwrite(pic_file,img)

dst ='/home/lixialin/Videos/pic'
if os.path.isdir(dst):
    shutil.rmtree(dst)
os.makedirs(dst,exist_ok=True)
# json_src_lable = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/01_json/front_2d_day_1920x1080'
json_src_perce = '/home/lixialin/Downloads/IHC_0403_result/camera_fusion'
pic_src = '/home/lixialin/Downloads/IHC_0403_result/front_near'
for root,_,files in os.walk(json_src_perce):
    files = sorted(files,key= lambda x: x.split('.')[0])
    for file_ in files:
        perce_json = os.path.join(root,file_)
        # lable_json = os.path.join(json_src_lable,'frame_vc2_' + str(int(file_.split('.')[0]))+'.json')
        # pic_file = os.path.join(pic_src,'frame_vc2_' + str(int(file_.split('.')[0]))+'.jpg')
        # lable_json = os.path.join(json_src_lable,str(int(file_.split('.')[0]))+'.json')
        pic_file = os.path.join(pic_src,str(int(file_.split('.')[0]))+'.jpg')
        perce_draw_box(perce_json,pic_file,dst)
        # pic_file1 = os.path.join(dst,'frame_vc2_' + str(int(file_.split('.')[0]))+'.jpg')
        # lable_draw_box(lable_json,pic_file1,dst)





