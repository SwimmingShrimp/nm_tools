from operator import ne
import os
import re
import argparse
from pathlib import Path
import re
import os.path as osp
import cv2
import numpy as np
import sys
sys.path.append("..")
import utils

argparser = argparse.ArgumentParser()
argparser.add_argument('srcpath',type=str)
args = argparser.parse_args()

src = args.srcpath
newfiles =[]
for root,files in utils.walk(src):
    for file_ in files:
        # if 'oimg' in root:
        newfiles.append(file_)

cv2.namedWindow('ViewPic',cv2.WINDOW_NORMAL)
idx = 0
while True:
    print(newfiles[idx])
    img = cv2.imread(files[idx])
    cv2.imshow('ViewPic',img)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    elif key == ord('b'):
        idx -= 1
    elif key == ord('k'):
        idx -=5
    elif key == ord('j'):
        idx -=15
    elif key == ord('l'):
        idx -=50
    elif key == ord('1'):
        idx +=5
    elif key == ord('2'):
        idx +=10
    elif key == ord('3'):
        idx +=20
    elif key == ord('4'):
        idx +=50
    elif key == ord('5'):
        idx +=100
    elif key == ord('6'):
        idx +=1000
    else:
        idx += 1

cv2.destroyAllWindows()

