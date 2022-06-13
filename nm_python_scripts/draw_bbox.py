import os
import cv2
import json

'''draw lable json，2d标注的（x,y）左上角点'''
json_src = 'C:/Users/李夏临/Desktop/test/frame_vc1_1181.json'
img_src = 'C:/Users/李夏临/Desktop/test/frame_vc1_1181.bmp'

with open(json_src,'r') as f:
    json_data = json.load(f)
json_data = json_data["task_vehicle"]
img = cv2.imread(img_src)
for i in range(len(json_data)):
    x = int(json_data[i]["tags"]["x"])
    y = int(json_data[i]["tags"]["y"])
    h = int(json_data[i]["tags"]["height"])
    w = int(json_data[i]["tags"]["width"])
    # cv2.rectangle(img, (int(x-w/2),int(y-h/2)), (int(x+w/2),int(y+h/2)),(0,255,255),1)
    cv2.rectangle(img, (x,y), ((x+w),(y+h)),(0,255,255),1)
cv2.namedWindow('img')
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows


# '''draw perce json,(x,y)左上角点'''
# json_src = '/home/NULLMAX/lixialin/文档/project/preception_side/obstacle_perception/build_infer/x86_linux/image_record/image_record_json/side_right_rear/frame_vc8_20.json'
# img_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Shangqi/2D_dataset/2batch/dataset_png_1080_b200/side_right_rear/frame_vc8_20.png'

# with open(json_src,'r') as f:
#     json_data = json.load(f)
# img = cv2.imread(img_src)
# proportion = 3.75
# for each in json_data["tracks"].items():
#     echo_value = each[1]["uv_bbox2d"]
#     h = int(echo_value["obstacle_bbox.height"]*proportion)
#     w = int(echo_value["obstacle_bbox.width"]*proportion)
#     x = int(echo_value["obstacle_bbox.x"]*proportion)
#     y = int((echo_value["obstacle_bbox.y"])*proportion+120)
#     cv2.rectangle(img, (x,y), (x+w,y+h),(0,255,0),1)
# cv2.namedWindow('img')
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows