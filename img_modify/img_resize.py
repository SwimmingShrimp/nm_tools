import os
import sys
sys.path.append("..")
import utils
import cv2

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/640x384_rename_bmp'

for root,files in utils.walk(src):
    dst = root.replace('640x384_rename_bmp','1920x1280_bmp')
    if not os.path.exists(dst):
        os.makedirs(dst)
    for file_ in  files:
        # print(file_)
        basename = os.path.basename(file_)
        img = cv2.imread(file_)
        # img = img[90:1242,0:1920]
        # img = cv2.resize(img, (640, 384))
        # img = cv2.resize(img, (1920, 1152))
        img = cv2.resize(img, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
        img = cv2.copyMakeBorder(img, 40, 88, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))        
        img_path = dst + '/' + basename
        # print(img_path)
        cv2.imwrite(img_path,img,)