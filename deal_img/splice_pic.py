import cv2
import numpy as np
import os

# ori_path = '/media/lixialin/lxl/00_data/0711_way_isp/20230713_145545'
ori_path = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/saic_side_2d_day/1920x1280_png'
endwith = '.png'

side_left_rear_path = os.path.join(ori_path,'side_left_rear')
side_left_front_path = os.path.join(ori_path,'side_left_front')
side_right_rear_path = os.path.join(ori_path,'side_right_rear')
side_right_front_path = os.path.join(ori_path,'side_right_front')

left_dst = os.path.join(ori_path,'side_left')
right_dst = os.path.join(ori_path,'side_right')
dst = os.path.join(ori_path,'side_img')
os.makedirs(left_dst,exist_ok=True)
os.makedirs(right_dst,exist_ok=True)
os.makedirs(dst,exist_ok=True)

for i in range(700,800,1):
    left_img1 = cv2.imread(os.path.join(side_left_rear_path,('frame_vc5_' + str(i) + endwith)))
    left_img2 = cv2.imread(os.path.join(side_left_front_path,('frame_vc6_' + str(i) + endwith)))
    right_img1 = cv2.imread(os.path.join(side_right_rear_path,('frame_vc8_' + str(i) + endwith)))
    right_img2 = cv2.imread(os.path.join(side_right_front_path,('frame_vc7_' + str(i) + endwith)))
    # left_img1 = cv2.imread(os.path.join(side_left_rear_path,(str(i) + endwith)))
    # left_img2 = cv2.imread(os.path.join(side_left_front_path,(str(i) + endwith)))
    # right_img1 = cv2.imread(os.path.join(side_right_rear_path,(str(i) + endwith)))
    # right_img2 = cv2.imread(os.path.join(side_right_front_path,(str(i) + endwith)))
    left_img =  np.hstack([left_img1,left_img2])
    right_img =  np.hstack([right_img2,right_img1])
    img = np.vstack([np.hstack([left_img2,right_img2]),np.hstack([left_img1,right_img1])])
    # cv2.imwrite(os.path.join(left_dst,(str(i) + endwith)),left_img)
    # cv2.imwrite(os.path.join(right_dst,(str(i) + endwith)),right_img)
    cv2.imwrite(os.path.join(dst,(str(i) + endwith)),img)