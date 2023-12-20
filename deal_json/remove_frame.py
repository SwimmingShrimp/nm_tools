# from genericpath import isdir
import sys
sys.path.append('..')
import utils
import os

for root,_,files in os.walk('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/saic_side_3d/jpg_1920x1080'):
    for file_ in files:
        newfile = str(int(file_.split("_")[-1].split(".")[0])) + '.jpg'
        os.system('mv {} {}'.format(os.path.join(root,file_),os.path.join(root,newfile)))