import os
import sys
sys.path.append('..')
import utils
import cv2

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/3D/1920x1080_png'
dst ='/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/3D/1920x1280_png'
os.makedirs(dst,exist_ok=True)

for root,files in utils.walk(src):
    for file_ in  files:
        img = cv2.imread(file_)
        file_= file_.replace(src,dst)
        print(file_)
        os.makedirs(os.path.dirname(file_),exist_ok=True)
        img = cv2.copyMakeBorder(img, 200, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        # img_crop = img[150:1230, 0:1920]
        cv2.imwrite(file_,img,)