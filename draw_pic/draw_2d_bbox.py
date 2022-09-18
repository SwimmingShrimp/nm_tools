import os
import cv2
import json
import sys
sys.path.append("..")
import config


'''lable和percetion结果都画,标注绿色，感知红色'''
lable_json_src = '/home/lixialin/Pictures/lable/qr_obj_test_20220906_0.json'
perce_json_src = '/home/lixialin/Pictures/camera_fusion/1547.json'
img_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/2D/new_night/1920x1080_png/FOV30/frame_vc2_1547.png'

with open(lable_json_src,'r') as f1,open(perce_json_src,'r') as f2:
    lable_json_data = json.load(f1)
    perce_json_data = json.load(f2)
    img = cv2.imread(img_src)
    proportion = 3
    if  perce_json_data[1]['FOV30']["tracks"]:
        for each in perce_json_data[1]["FOV30"]["tracks"]:
            echo_value = each["uv_bbox2d"]
            h = int(echo_value["obstacle_bbox.height"]*proportion)
            w = int(echo_value["obstacle_bbox.width"]*proportion)
            x = int(echo_value["obstacle_bbox.x"]*proportion)
            y = int((echo_value["obstacle_bbox.y"])*proportion-160)
            perce_type_value = each["obstacle_type"]
            perce_type = config.front_config["enum_obstacle1"][perce_type_value][:3]
            cv2.rectangle(img, (x,y), (x+w,y+h),(0,0,255),1)
            cv2.putText(img,perce_type,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    lable_json_data = lable_json_data
    for temp in lable_json_data:
        if temp['filename'] == 'frame_vc2_1547.png':
            for temp1 in temp["task_vehicle"]:
                x = int(temp1["tags"]["x"])
                y = int(temp1["tags"]["y"])
                h = int(temp1["tags"]["height"])
                w = int(temp1["tags"]["width"])
                lable_type = temp1["tags"]["class"][:3]
                # cv2.rectangle(img, (int(x-w/2),int(y-h/2)), (int(x+w/2),int(y+h/2)),(0,255,255),1)
                cv2.rectangle(img, (x,y), ((x+w),(y+h)),(0,255,0),1)
                cv2.putText(img,lable_type,(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
cv2.namedWindow('img')
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows   