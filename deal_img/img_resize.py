import os
import sys
sys.path.append("..")
import utils
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str,help='the position of the src picture')
parser.add_argument('dst',type=str,help='the position of the dst picture')
args = parser.parse_args()

src = args.src
dst = args.dst


for root,files in utils.walk(src):
    for file_ in  files:
        basename = os.path.basename(file_)
        img = cv2.imread(file_)
        # 直接缩放到固定大小，无特定比例
        img = img[40:1480,0:3840]
        img = cv2.resize(img, (1280, 480))
        # img = cv2.copyMakeBorder(img, 100, 100, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        '''
        resize(InputArray src, OutputArray dst, Size dsize, double fx=0, double fy=0, int interpolation=INTER_LINEAR )
        fx:宽，fy:高
        interpolation：插值。图像缩放之后，肯定像素要进行重新计算的，就靠这个参数来指定重新计算像素的方式，有以下几种：
            INTER_NEAREST - 最邻近插值
            INTER_LINEAR - 双线性插值，如果最后一个参数你不指定，默认使用这种方法
            INTER_CUBIC - 4x4像素邻域内的双立方插值
            INTER_LANCZOS4 - 8x8像素邻域内的Lanczos插值
        '''
        # 缩放几倍，
        # img = cv2.resize(img, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        dst_file = file_.replace(src,dst)
        os.makedirs(os.path.dirname(dst_file),exist_ok=True)       
        cv2.imwrite(dst_file,img,)