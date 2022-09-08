import os
import sys
sys.path.append('..')
import utils
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str,help='the position of the src picture')
parser.add_argument('dst',type=str,help='the position of the dst picture')
args = parser.parse_args()

src = args.src
dst = args.dst
os.makedirs(dst,exist_ok=True)

for root,files in utils.walk(src):
    for file_ in  files:
        img = cv2.imread(file_)
        file_= file_.replace(src,dst)
        print(file_)
        os.makedirs(os.path.dirname(file_),exist_ok=True)
        img = cv2.copyMakeBorder(img, 200, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        cv2.imwrite(file_,img,)
