import os
import sys
sys.path.append('..')
import utils
import imagesize
import cv2

with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/imgsize.txt','r') as f:
    for line in f.readlines():
        imgpath,imgsize = line.strip().split('|')
        if imgsize=='3840x2160':
            continue
        elif imgsize=='1920x1080':
            img = cv2.imread(imgpath)
            img = cv2.resize(img, (3840, 2160))       
            cv2.imwrite(imgpath,img,)
        elif imgsize=='1920x1280':
            img = cv2.imread(imgpath)
            img = img[0:1080,0:1920]
            img = cv2.resize(img, (3840, 2160))       
            cv2.imwrite(imgpath,img,)

for root,files in utils.walk('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/rename_3840x2160'):
        for file_ in files:
            width,height = imagesize.get(file_)
            if int(width)!=3840:
                print(file_)

for root, dirs, files in os.walk('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/rename_3840x2160'):
    for file_ in files:
        if file_.endswith('.jpg'):
            continue
        elif file_.endswith('.png'):
            dst_file = file_.replace('.png','.jpg')
        elif file_.endswith('.bmp'):
            dst_file = file_.replace('.bmp','.jpg')
        command = 'ffmpeg -i {} {}'.format(os.path.join(root,file_),os.path.join(root,dst_file))
        os.system(command)