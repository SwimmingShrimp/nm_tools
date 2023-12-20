import os
import cv2
import json
import sys
sys.path.append("..")
import config

def draw_perce_box(perce_json_src,pic_src,dst):
    with open(perce_json_src,'r') as f2:
        # lable_json_data = json.load(f1)
    # with open(perce_json_src,'r') as f2:    
        perce_json_data = json.load(f2)
        img = cv2.imread(pic_src)
        pic_name = os.path.basename(pic_src)
        top_cut = 40
        proportion_h = 3
        proportion_z = 3
        if  perce_json_data[5]['front_far_traffic_sign']["detect_result"]:
            for each in perce_json_data[5]["front_far_traffic_sign"]["detect_result"]:
                x = int(each[0]*proportion_h)
                y = int(each[1]*proportion_h) + top_cut
                w = int(each[2]*proportion_h)
                h = int(each[3]*proportion_h)
                cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255),3)
                perce_type = config.front_config["enum_tsr"][int(each[4])]
                cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                if round(each[5],3) > 0.5:
                    cv2.putText(img,'min',(x-40,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                # if round(each[5],3) < 0.5:
                #     cv2.putText(img,'max',(x-40,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                if round(each[6],3) > 0.5:
                    cv2.putText(img,'cancel',(x-40,y+h+40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                if round(each[7],3) > 0.5:
                    cv2.putText(img,'led',(x-40,y+h+60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                if round(each[8],3) > 0.5:
                    cv2.putText(img,'ring',(x-40,y+h+80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        # cv2.namedWindow('img',cv2.WINDOW_KEEPRATIO)
        # cv2.imshow('img',img)
            print(os.path.join(dst,pic_name))
            cv2.imwrite(os.path.join(dst,pic_name),img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows   
def draw_lable_box(lable_json_src,pic):
    img = cv2.imread(pic)
    json_name = os.path.basename(pic).replace('.jpg','.json')
    lable_json_src = os.path.join(lable_json_src,json_name)
    with open(lable_json_src,'r') as f2 :
        lable_json_data = json.load(f2)
        if  lable_json_data['traffic_light']:
            for each in lable_json_data['traffic_light']:
                x = int(each["xywh"][0])*2
                y = int(each["xywh"][1])*2
                w = int(each["xywh"][2])*2
                h = int(each["xywh"][3])*2
                x = int(x-w/2)
                y = int(y-h/2)
                cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),3)
                if each["attrs"]["shape"][0].endswith("arrow"):
                    shape_type = config.front_config["enum_tl_shape_type"]['arrow']
                else:
                    shape_type = config.front_config["enum_tl_shape_type"][each["attrs"]["shape"][0]]
                froward = config.front_config["enum_tl_direct"][each["attrs"]["direction"]["forward"]]
                left = config.front_config["enum_tl_direct"][each["attrs"]["direction"]["left"]]
                right = config.front_config["enum_tl_direct"][each["attrs"]["direction"]["right"]]
                uturn = config.front_config["enum_tl_direct"][each["attrs"]["direction"]["uturn"]]
                lable_type = str(shape_type) + '_' + str(froward) + '_' + str(left) + '_' + str(right) + '_' +str(uturn)
                cv2.putText(img,lable_type,(x+w-20,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.imwrite(pic,img)


dst ='/home/lixialin/Music'
# lable_json_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/lable_json/FOV30'
perce_src_json = '/home/lixialin/Pictures/perce_json/front_far'
src_pic = '/home/lixialin/Pictures/gt_ori/front_far'
for root,_,files in os.walk(perce_src_json):
    for file_ in files:
        perce_json_src = os.path.join(root,file_)
        pic_path = root.replace(perce_src_json,src_pic)
        pic = str(int(file_.split('.')[0])) + '.jpg'
        pic_src = os.path.join(pic_path,pic)
        print(pic_src)
        draw_perce_box(perce_json_src,pic_src,dst)
        # draw_lable_box(lable_json_src,os.path.join(dst,pic))


