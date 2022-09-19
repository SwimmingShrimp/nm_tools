import os
import argparse
import sys
sys.path.append("..")
import utils
import undist_nullmax_jyf
import cv2  
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('src',type=str,help='fov30 pic')
parser.add_argument('dst',type=str)
args = parser.parse_args()

src = args.src
dst = args.dst

'''跑前确认video解压下来的名称相同'''
def download_data():
    for root, files in utils.walk(src):
        for file_ in files:
            num = os.path.basename(file_).split('_')[-1].split('.')[0]
            # num = os.path.basename(file_).split('.')[0]
            file_120 = file_.replace('fov_30','fov_120')
            file_120 = file_120.replace('vc1','vc2')
            if int(num)<10000:
                dst1 = os.path.join(dst,'1','FOV30')
                dst11 = os.path.join(dst,'1','FOV120')
                os.makedirs(dst1,exist_ok=True)
                os.makedirs(dst11,exist_ok=True)
                os.system('cp {} {}'.format(file_,dst1,))
                os.system('cp {} {}'.format(file_120,dst11,))
            elif 10000<=int(num)<20000:
                dst2 = os.path.join(dst,'2','FOV30')
                dst21 = os.path.join(dst,'2','FOV120')
                os.makedirs(dst2,exist_ok=True)
                os.makedirs(dst21,exist_ok=True)
                os.system('cp {} {}'.format(file_,dst2,))
                os.system('cp {} {}'.format(file_120,dst21,))
            elif 20000<=int(num)<30000:
                dst3 = os.path.join(dst,'3','FOV30')
                dst31 = os.path.join(dst,'3','FOV120')
                os.makedirs(dst3,exist_ok=True)
                os.makedirs(dst31,exist_ok=True)
                os.system('cp {} {}'.format(file_,dst3,))
                os.system('cp {} {}'.format(file_120,dst31,))
            elif 30000<=int(num)<40000:
                dst4 = os.path.join(dst,'4','FOV30')
                dst41 = os.path.join(dst,'4','FOV120')
                os.makedirs(dst4,exist_ok=True)
                os.makedirs(dst41,exist_ok=True)
                os.system('cp {} {}'.format(file_,dst4,))
                os.system('cp {} {}'.format(file_120,dst41,))   
            elif 40000<=int(num)<50000:
                dst5 = os.path.join(dst,'5','FOV30')
                dst51 = os.path.join(dst,'5','FOV120')
                os.makedirs(dst5,exist_ok=True)
                os.makedirs(dst51,exist_ok=True)
                os.system('cp {} {}'.format(file_,dst5,))
                os.system('cp {} {}'.format(file_120,dst51,))

def check_pic_normal():
    err_txt_path = os.path.join(dst,'err_pic.txt')
    with open(err_txt_path,'a+') as f:
        for root,files in utils.walk(dst):
            for i in range(len(files)):
                try:
                    Image.open(files[i]).load()
                # except SyntaxError as e:
                except:
                    comment = files[i] + '\n'
                    command = 'cp {} {}'.format(files[i-1],files[i])
                    print(command)
                    os.system(command)
                    f.write(comment)

def complete_black_edge():
    for root,files in utils.walk(dst):
        for file_ in  files:
            if 'FOV30' in root or 'FOV120_undist' in root:
                img = cv2.imread(file_)
                os.makedirs(os.path.dirname(file_),exist_ok=True)
                # cv2.copyMakeBorder(src,top,bottom,left,right,borderType,value)
                img = cv2.copyMakeBorder(img, 200, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                cv2.imwrite(file_,img,)

def rename_pic():
    for root,files in utils.walk(dst):
        for file_ in  files:
            if 'FOV30' in root:
                new_file = file_.replace('vc1','vc2')
            elif 'FOV120_undist' in root:
                new_file = file_.replace('vc2','vc1')
            else:
                continue
            os.system('mv {} {}'.format(file_,new_file))      

def main():
    # download_data()
    # check_pic_normal()
    # undist_nullmax_jyf.undist_120(dst)
    # complete_black_edge()
    rename_pic()

if __name__=='__main__':
    main()
