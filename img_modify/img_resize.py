import os
import sys
sys.path.append("..")
import utils
import cv2

src = '/home/NULLMAX/lixialin/视频/static_obstacle/640x384_bmp'

for root,files in utils.walk(src):
    dst = root.replace('640x384_bmp','1920x1280_bmp')
    if not os.path.exists(dst):
        os.makedirs(dst)
    for file_ in  files:
        # print(file_)
        basename = os.path.basename(file_)
        img = cv2.imread(file_)
        img = cv2.resize(img, (1920, 1152))
        img = cv2.copyMakeBorder(img, 90, 38, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        img_path = dst + '/' + basename
        # print(img_path)
        cv2.imwrite(img_path,img,)