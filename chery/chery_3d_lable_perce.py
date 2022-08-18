import json
import os
from tqdm import tqdm
import sys
sys.path.append("..")
import utils
import cv2
import config
import numpy as np


#定义图片位置、标注json位置、算法推理json位置、可视化结果存放位置
img_path = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/3D/1920x1080_png/FOV30'
lable_json_path = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/1_json/chery/3d_lable_merge'
perce_json_path = '/home/lixialin/Videos/camera_fusion'
results_path = '/home/lixialin/Videos/results'
os.makedirs(results_path,exist_ok=True)
#定义bev的长宽,图片长宽1920x1080
bev_w = 126
bev_l = 1080

def draw_lable_2d(img,lable_json):
    # 绿色
    json_data = utils.get_json_data(os.path.join(lable_json_path,lable_json))
    for temp in json_data:
        type_2d = temp["type"][:3]
        x = int(temp["box_2d"]["x"])
        y = int(temp["box_2d"]["y"])
        w = int(temp["box_2d"]["w"])
        h = int(temp["box_2d"]["h"])
        cv2.rectangle(img, (x,y), ((x+w),(y+h)), (0,255,0),1)
        cv2.putText(img, type_2d, (x, (y-10)), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    return img

def draw_perce_2d(img,perce_json):
    # 红色
    perce_data = utils.get_json_data(os.path.join(perce_json_path,perce_json))
    multiple = 3
    for temp in perce_data[0]["front_far"]["tracks"]:
        type_value = temp["obstacle_type"]
        type_3d = config.front_config["enum_obstacle1"][type_value][:3]
        x = int(temp["uv_bbox2d"]["obstacle_bbox.x"]) * multiple
        y = int(temp["uv_bbox2d"]["obstacle_bbox.y"]) * multiple -160
        w = int(temp["uv_bbox2d"]["obstacle_bbox.width"]) * multiple
        h = int(temp["uv_bbox2d"]["obstacle_bbox.height"])* multiple
        cv2.rectangle(img, (x,y), ((x+w),(y+h)),(0,0,255),1)
        cv2.putText(img, type_3d, (x, (y+h+15)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
    return img

def draw_lable_bev(img,lable_json):
    multiple = 4
    json_data = utils.get_json_data(os.path.join(lable_json_path,lable_json))
    for temp in json_data:
        type_2d = temp["type"][:3]
        yaw = temp["orientation"]["y"]
        dist_x = int(temp["position"]["x"]*multiple)
        dist_y = int(temp["position"]["y"]*multiple)
        l = int(temp["dimension"]["x"]*multiple)
        w = int(temp["dimension"]["y"]*multiple)
        x = int(bev_w/2 - dist_y)
        y = int(bev_l - dist_x*multiple -l)
        cv2.rectangle(img,(x,y),((x+w),(y+l)),(0,255,0),-1)
        cv2.putText(img, type_2d, (x, (y-10)), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1)
    return img


def draw_perce_bev(img,perce_json):
    perce_data = utils.get_json_data(os.path.join(perce_json_path,perce_json))
    multiple = 4
    for temp in perce_data[0]["front_far"]["tracks"]:
        type_value = temp["obstacle_type"]
        type_3d = config.front_config["enum_obstacle1"][type_value][:3]
        yaw = temp["bbox3d"]["obstacle_heading_yaw"]
        dist_x = int(temp["bbox3d"]["obstacle_pos_x"]*multiple)
        dist_y = int(temp["bbox3d"]["obstacle_pos_y"]*multiple)
        l = int(temp["obstacle_length"]*multiple)
        w = int(temp["obstacle_width"]*multiple)
        x = int(bev_w/2 - dist_y)
        y = int(bev_l - dist_x*multiple -l)
        cv2.rectangle(img,(x,y),((x+w),(y+l)),(0,0,255),-1)
        cv2.putText(img, type_3d, ((x), (y+l+15)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
    return img    

def draw_figure(img):
    # 竖向网格
    for m in range(0, bev_w,18):
        cv2.line(img, (0+m,0), (0+m,bev_l), color=(170, 170, 170), thickness=1)
    # 横向网格
    for m in range(0,bev_l,45):
        cv2.line(img, (0, 0+m), (bev_w, 0+m), color=(170, 170, 170), thickness=1)
    cv2.rectangle(img, (int(bev_w/2-5), int(bev_l-20)), (int(bev_w/2+5), int(bev_l)), (255,165,0), -1)
    return img

def main():
    lable_json_list = []
    for root,_, files in os.walk(lable_json_path):
        files.sort(key=lambda x:int(x.split('.')[0]))
    lable_json_list = files
    for i in tqdm(range(len(lable_json_list))):
        filename ='frame_vc2_' + (lable_json_list[i]).replace('json','png')
        perce_json_name = (lable_json_list[i].split('.')[0]).zfill(4) + '.json'
        img_2d = cv2.imread(os.path.join(img_path,filename))
        #在图片上画2D框
        img_2d = draw_lable_2d(img_2d,lable_json_list[i])
        img_2d = draw_perce_2d(img_2d,perce_json_name)
        img_bev = np.zeros((bev_l, bev_w, 3), np.uint8)
        img_bev.fill(200)
        img_bev = draw_figure(img_bev)
        img_bev = draw_lable_bev(img_bev,lable_json_list[i])
        img_bev = draw_perce_bev(img_bev,perce_json_name)
        img = np.hstack([img_2d, img_bev])
        cv2.imwrite(os.path.join(results_path,filename),img)
        cv2.namedWindow('img')
        cv2.imshow('img',img)
        cv2.waitKey(10)
        cv2.destroyAllWindows


if __name__=='__main__':
    main()