import os
import cv2
import json
import sys
sys.path.append("../..")
import config

def draw_perce_box(perce_json_src,pic_src,dst):
    with open(perce_json_src,'r') as f2:    
        perce_json_data = json.load(f2)
        img = cv2.imread(pic_src)
        pic_name = os.path.basename(pic_src)
        top_cut = 180
        proportion_h = 3
        proportion_z = 3
        if  perce_json_data[6]['front_far_traffic_sign']["detect_result"]:
            for each in perce_json_data[6]["front_far_traffic_sign"]["detect_result"]:
                x = int(each[0]*proportion_h)
                y = int(each[1]*proportion_h) + top_cut
                w = int(each[2]*proportion_h)
                h = int(each[3]*proportion_h)
                cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255),3)
                # perce_type =  str(each[4]) + '_' + str(each[6]) + '_' + str(each[8]) + '_' + str(each[10]) + '_' + str(each[12])
                # cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        # cv2.namedWindow('img',cv2.WINDOW_KEEPRATIO)
        # cv2.imshow('img',img)
            print(os.path.join(dst,pic_name))
            cv2.imwrite(os.path.join(dst,pic_name),img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows   
def draw_gt_box(gt_json,pic):
    img = cv2.imread(pic)
    with open(gt_json,'r') as f2 :
        lable_json_data = json.load(f2)
        if  lable_json_data[3]['front_far_traffic_light']:
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


pic_path = '/home/lixialin/Music/pic'
dst_path ='/home/lixialin/Music'
perce_json_path = '/home/lixialin/Music/gt_json'
for root,_,files in os.walk(pic_path):
    for file_ in files:
        perce_json = os.path.join(root.replace(pic_path,perce_json_path),file_.replace('.jpg','.json'))
        pic = os.path.join(root,file_)
        draw_perce_box(perce_json,pic,dst_path)


