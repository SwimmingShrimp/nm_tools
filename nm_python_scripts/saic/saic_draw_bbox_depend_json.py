import os
import cv2
import json

'''draw lable json，（x,y）中心点'''
json_src = '/home/NULLMAX/lixialin/视频/json/new_json/day/day.json'
img_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Shangqi/2D_dataset/2batch/dataset_t150_b50/side_left_rear/frame_vc5_54.png'



with open(json_src,'r') as f:
    json_data = json.load(f)
# # json_data = json_data["tracks"]

img = cv2.imread(img_src)
# for each in json_data.values():
#     echo_value = each["uv_bbox2d"]
#     h = int(echo_value["obstacle_bbox.height"]*3.75)
#     w = int(echo_value["obstacle_bbox.width"]*3.75)
#     x = int(echo_value["obstacle_bbox.x"]*3.75)
#     y = int((echo_value["obstacle_bbox.y"])*3.75+120)
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
    # print((x, y), (x+w, y-h))

for temp in json_data:
    if temp["filename"]=='frame_vc5_54.png':
        json_data1 =temp["task_vehicle"]
        print(json_data1)
        for temp1 in json_data1:
            x = int(temp1["tags"]["x"])
            y = int(temp1["tags"]["y"]) -150
            h = int(temp1["tags"]["height"])
            w = int(temp1["tags"]["width"])
            # cv2.rectangle(img, (int(x-w/2),int(y-h/2)), (int(x+w/2),int(y+h/2)),(0,255,255),1)
            cv2.rectangle(img, (int(x),int(y)), (int(x+w),int(y+h)),(0,255,255),1)



# cv2.rectangle(img,(x,y),(1185,720),(0,255,255),1)

cv2.namedWindow('img')
cv2.imshow('img',img)
cv2.waitKey(0)
# cv2.destroyAllWindows


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

# json_data = json_data["tracks"]
# for each in json_data.values():
#     echo_value = each["uv_bbox2d"]
#     h = int(echo_value["obstacle_bbox.height"]*3.75)
#     w = int(echo_value["obstacle_bbox.width"]*3.75)
#     x = int(echo_value["obstacle_bbox.x"]*3.75)
#     y = int((echo_value["obstacle_bbox.y"])*3.75+120)
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)
#     print((x, y), (x+w, y-h))


# cv2.namedWindow('img')
# cv2.imshow('img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows