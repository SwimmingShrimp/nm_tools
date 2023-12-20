from ntpath import join
import os
import cv2
import json
import sys
sys.path.append('../..')
import config
import utils

dst_perce ='/home/lixialin/Downloads'
dst_gt ='/home/lixialin/Videos/pic/gt'
os.makedirs(dst_perce,exist_ok=True)
os.makedirs(dst_gt,exist_ok=True)
json_src_lable = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/01_json/saic_side_2d_day/side_right_front'
json_src_perce = '/home/lixialin/Downloads/image_record/image_record_json/camera_fusion'
pic_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/saic_side_2d_day/1920x1080_jpgjpg'
# def draw_gt():
#     for root,_,files in os.walk(json_src_lable):
#         for file_ in files:
#             pic_file = os.path.join(pic_src,str(int(file_.split('.')[0]))+'.jpg')
#             img = cv2.imread(pic_file)
#             pic_name = os.path.basename(pic_file)
#             gt_json_data = utils.get_json_data(os.path.join(root,file_))
#             if  gt_json_data['task_vehicle']:
#                 for each in gt_json_data['task_vehicle']:
#                     x = int(each["tags"]["x"])
#                     y = int(each["tags"]["y"]) - 200
#                     w = int(each["tags"]["width"])
#                     h = int(each["tags"]["height"])
#                     lable_type = each["tags"]["class"]
#                     cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),3)
#                     cv2.putText(img,lable_type,(x+w-20,y+h+20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
#                 cv2.imwrite(os.path.join(dst_gt,pic_name),img)

def draw_perce():
    for root,_,files in os.walk(json_src_perce):
        for file_ in files:
            camera_name = "side_right_front"
            perce_json = os.path.join(root,file_)
            pic_file = os.path.join(pic_src,camera_name,'frame_vc7_' + str(int(file_.split('.')[0]))+'.jpg')
            print(pic_file)
            pic_name = os.path.basename(pic_file)
            img = cv2.imread(pic_file)            
            top_cut = 120
            top_ori = 200
            top_black = 0
            proportion = 3.75
            with open(perce_json,'r') as f2: 
                perce_json_data = json.load(f2)
                for i in range(len(perce_json_data)):
                    if camera_name in perce_json_data[i]:
                        camera_idx = i
                if  perce_json_data[camera_idx][camera_name]["detect_result"]:
                    for each in perce_json_data[camera_idx][camera_name]["detect_result"]:
                        x = int(each[2]*proportion)
                        y = int(each[3]*proportion) + top_cut -top_black
                        x1 = int(each[4]*proportion)
                        y1 = int(each[5]*proportion) + top_cut -top_black
                        cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),3)
                        perce_type = config.front_config["enum_obstacle1"][int(each[0])]
                        cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    cv2.imwrite(os.path.join(dst_perce,pic_name),img)
# draw_gt()
draw_perce()
