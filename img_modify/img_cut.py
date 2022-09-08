import os
import cv2
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str,help='the position of the src picture')
parser.add_argument('dst',type=str,help='the position of the dst picture')
args = parser.parse_args()

src = args.src
dst = args.dst


for root, files in utils.walk(src):
    for file_ in files:
        print(file_)
        img = cv2.imread(file_)
        #img[宽开始：结束，高开始：结束]
        img_crop = img[200:1280,0:1920]
        dst_file = file_.replace(src,dst)
        dst_path = os.path.dirname(dst_file) 
        os.makedirs(dst_path,exist_ok=True)      
        cv2.imwrite(file_, img_crop,)




        

