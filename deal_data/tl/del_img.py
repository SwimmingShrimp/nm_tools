import os
import sys
sys.path.append('..')
import utils
import imagesize
import cv2

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/traffic_light_benchmark/IMAGE'
with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/traffic_light_benchmark/relation.txt','a+') as f:
    for root,_,files in os.walk(src):
        for file_ in files:
            if not file_.endswith('.jpg'):
                print(file_)
            imgfile = os.path.join(root,file_)
            width,height = imagesize.get(imgfile)
            comment = imgfile + '|' + str(width) + 'x' + str(height)
            if height!=1080:
                print(comment)

