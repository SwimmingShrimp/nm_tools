import os
import cv2
import json
import sys
sys.path.append('../..')
import utils
import config
import shutil

pic_src = '/home/lixialin/Downloads/image/front_near'
pic_dst = '/home/lixialin/Videos/pic'
if os.path.isdir(pic_dst):
    shutil.rmtree(pic_dst)
os.makedirs(pic_dst,exist_ok=True)

for root,_,files in os.walk(pic_src):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        img = cv2.imread(os.path.join(root,file_))
        # cv2.line(img,(0,180),(3840,180),(0,0,255),2)
        # cv2.line(img,(0,1620),(3840,1560),(0,0,255),2)
        cv2.line(img,(0,40),(3840,40),(0,0,255),2)
        cv2.line(img,(0,1480),(3840,1480),(0,0,255),2)

        cv2.imwrite(os.path.join(pic_dst,file_),img)
