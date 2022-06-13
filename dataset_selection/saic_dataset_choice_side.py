import os
import re
import argparse
import glob
from pathlib import Path
import re
import os.path as osp
import cv2
import numpy as np
import utils

src = '/data1/NMtest/DataChoice/ShangQi/20220426/ori/2022-02-27'
dataset_dst = '/data1/NMtest/DataChoice/ShangQi/20220426/dataset/2022-02-27'
lable_dst = '/data1/NMtest/DataChoice/ShangQi/20220426/lable/2022-02-27'


path1 = []
path2 = []
path3 = []
path4 = []

for root,files in utils.walk(src):
    for file_ in files:
        if 'SideFrontLeft' in file_:
            path1.append(file_)
            path2.append(file_.replace('SideFrontLeft','SideFrontRight'))
            path3.append(file_.replace('SideFrontLeft','SideRearLeft'))
            path4.append(file_.replace('SideFrontLeft','SideRearRight'))

cv2.namedWindow('ViewPic',cv2.WINDOW_NORMAL)
idx = 0
while True:
    print(path1[idx])
    img1 = cv2.imread(path1[idx])
    img2 = cv2.imread(path2[idx])
    img3 = cv2.imread(path3[idx])
    img4 = cv2.imread(path4[idx])
    img = np.vstack([np.hstack([img1, img2]), np.hstack([img3, img4])])
    cv2.imshow('ViewPic',img)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    elif key == ord('b'):
        idx -= 1
    elif key == ord('s'):
        # for i in range(idx-16,idx+15):
        # print('cp {} {}/side_left_front'.format(path1,dst))
        dst1 = (os.path.dirname(path1[idx])).replace(src,dataset_dst)
        dst2 = (os.path.dirname(path2[idx])).replace(src,dataset_dst)
        dst3 = (os.path.dirname(path3[idx])).replace(src,dataset_dst)
        dst4 = (os.path.dirname(path4[idx])).replace(src,dataset_dst)
        print(dst1)
        if not os.path.exists(dst1):
            os.makedirs(dst1)
        if not os.path.exists(dst2):
            os.makedirs(dst2)
        if not os.path.exists(dst3):
            os.makedirs(dst3)
        if not os.path.exists(dst4):
            os.makedirs(dst4)
        os.system('cp {} {}'.format(path1[idx],dst1))
        os.system('cp {} {}'.format(path2[idx],dst2))
        os.system('cp {} {}'.format(path3[idx],dst3))
        os.system('cp {} {}'.format(path4[idx],dst4))
    elif key == ord('5'):
        dst5 = (os.path.dirname(path3[idx])).replace(src,lable_dst)
        print(dst5)
        if not os.path.exists(dst5):
            os.makedirs(dst5)
        os.system('cp {} {}'.format(path3[idx],dst5))
    elif key == ord('6'):
        dst6 = (os.path.dirname(path1[idx])).replace(src,lable_dst)
        print(dst6)
        if not os.path.exists(dst6):
            os.makedirs(dst6)
        os.system('cp {} {}'.format(path1[idx],dst6))
    elif key == ord('7'):
        dst7 = (os.path.dirname(path2[idx])).replace(src,lable_dst)
        print(dst7)
        if not os.path.exists(dst7):
            os.makedirs(dst7)
        os.system('cp {} {}'.format(path2[idx],dst7))
    elif key == ord('8'):
        dst8 = (os.path.dirname(path4[idx])).replace(src,lable_dst)
        print(dst8)
        if not os.path.exists(dst8):
            os.makedirs(dst8)
        os.system('cp {} {}'.format(path4[idx],dst8))
    else:
        idx += 1

cv2.destroyAllWindows()

