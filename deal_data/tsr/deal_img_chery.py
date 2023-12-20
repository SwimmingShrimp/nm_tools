import os
import sys
sys.path.append('..')
import utils
import imagesize
import cv2

def modify_img_size(dst):
    with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/relation.txt','r') as f:
        for line in f.readlines():
            ori_imgpath,rename_imgpath,imgsize = line.strip().split('|')
            img = cv2.imread(ori_imgpath)
            dst_path = os.path.join(dst,rename_imgpath)
            if imgsize=='3840x2160':
                img = cv2.resize(img, (1920, 1080))
                img = cv2.copyMakeBorder(img, 100, 100, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))      
                cv2.imwrite(dst_path,img,)
            elif imgsize=='1920x1080':
                img = cv2.copyMakeBorder(img, 100, 100, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))      
                cv2.imwrite(dst_path,img,)
            elif imgsize=='1920x1280':
                cv2.imwrite(dst_path,img,)

def modify_img_format(dst):
    for root,_,files in os.walk(dst):
        for file_ in files:
            if file_.endswith('.bmp'):
                newfilename = file_.replace('bmp','png')
                command = 'ffmpeg -i {} {}'.format(os.path.join(root,file_),os.path.join(dst,newfilename))
                os.system(command)
            elif file_.endswith('.jpg'):
                newfilename = file_.replace('jpg','png')
                command = 'ffmpeg -i {} {}'.format(os.path.join(root,file_),os.path.join(dst,newfilename))
                os.system(command)

dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/chery_rename_1920x1280'
# modify_img_size(dst)
modify_img_format(dst)