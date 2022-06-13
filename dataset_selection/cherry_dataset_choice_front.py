import os
import re
import argparse
import glob
from pathlib import Path
import re
import os.path as osp
import cv2
import numpy as np
import utils

argparser = argparse.ArgumentParser()
argparser.add_argument('srcpath',type=str)
argparser.add_argument('dstpath',type=str)
args = argparser.parse_args()

src = args.srcpath
dst = args.dstpath
if not os.path.exists(dst):
    os.makedirs(dst)

for root,files in utils.walk(src):
    pass

cv2.namedWindow('ViewPic',cv2.WINDOW_NORMAL)
idx = 0
while True:
    print(files[idx])
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
    elif key == ord('7'):
        idx +=10000
    elif key == ord('s'):
        os.system('cp {} {}'.format(files[idx],dst))
    else:
        idx += 1

cv2.destroyAllWindows()

