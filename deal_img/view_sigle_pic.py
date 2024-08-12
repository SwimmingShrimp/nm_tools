'''
Author: lixialin lixialin@nullmax.ai
Date: 2023-12-20 14:14:05
LastEditors: lixialin lixialin@nullmax.ai
LastEditTime: 2024-06-13 21:24:48
'''
from operator import ne
import os
import re
import argparse
from pathlib import Path
import re
import os.path as osp
import cv2
import numpy as np
import glob

argparser = argparse.ArgumentParser()
argparser.add_argument('srcpath',type=str)
argparser.add_argument('deletepath',type=str)
args = argparser.parse_args()

src = args.srcpath
delete = args.deletepath
newfiles =[]

#遍历文件下所有文件，返回函数walks： for root,files in walks(src):  files返回绝对路径+文件，且已从小到大排序
imgtypes = ['.jpg', '.bmp', '.png', '.yuv','.pcd']
def usort(fnames):
    if isinstance(fnames, dict):
        fnames = dict(sorted(fnames.items(), key=lambda k: int(re.sub(r'[^0-9]', '', k[0]))))
    elif isinstance(fnames, list):
        if len(fnames) and re.sub(r'[^0-9]', '', fnames[0]) != '':
            if isinstance(fnames[0], list):
                fnames = sorted(fnames, key=lambda k:int(re.sub(r'[^0-9]', '', k[0])))
            elif isinstance(fnames[0], dict):
                fnames = dict(sorted(fnames.items(), key=lambda k:int(re.sub(r'[^0-9]', '', k))))
            else:
                # if 'Side' in fnames[0]:
                #     print(int(fnames[0].split('/')[-1].split('-')[1] + fnames[0].split('/')[-1].split('-')[1]))
                #     fnames = sorted(fnames, key=lambda fname:int(fname.split('/')[-1].split('-')[1] + fname.split('/')[-1].split('-')[0]))
                # else:
                fnames = sorted(fnames, key=lambda fname:int(re.sub(r'[^0-9]', '', fname)))
            return fnames
    else:
        pass
    return fnames
def walk(p, regex='**/*'):
    regex = '**/*' if regex == '*' else regex
    fpaths = glob.glob('{}/{}'.format(p, regex), recursive=True)
    fpaths = [fpath for fpath in fpaths if fpath[-4:] in imgtypes]
    # print('==> Number: {:<6d}, Path: {}'.format(len(fpaths), '{}/{}'.format(osp.abspath(p), regex)))
    assert(len(fpaths)), 'No images in p: {}'.format(p)
    if fpaths:
        walks = {}
        for fpath in fpaths:
            dirpath = Path(fpath).parent.as_posix()
            if dirpath not in walks:
                walks[dirpath] = [fpath]
            else:
                walks[dirpath].append(fpath)

        for dirpath, fpaths in walks.items():
            try:
                walks[dirpath] = usort(fpaths)
            except:
                walks[dirpath] = fpaths
        try:
            walks = usort(walks).items()
        except:
            print('    !!!Sort error!!!')
            walks = walks.items()
    return walks

for root,files in walk(src):
    for file_ in files:
        # if 'oimg' in root:
        newfiles.append(file_)

cv2.namedWindow('ViewPic',cv2.WINDOW_NORMAL)
idx = 0
restore_pic_list = []
while True:
    print(newfiles[idx])
    img = cv2.imread(files[idx])
    cv2.imshow('ViewPic',img)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    elif key == ord('b'):
        idx -= 1
    elif key == ord('d'):
        delete_ = os.path.dirname(newfiles[idx].replace(src,delete))
        back_pic = newfiles[idx].replace(src,delete)
        back_path = os.path.dirname(newfiles[idx])
        restore_pic_list.append([back_path,back_pic])
        print(restore_pic_list)
        os.makedirs(delete_,exist_ok=True)
        os.system('mv {} {}'.format(newfiles[idx],delete_))
        idx +=1
    elif key == ord('r'):
        if len(restore_pic_list)>1:
            os.system('mv {} {}'.format(restore_pic_list[-1][1],restore_pic_list[-1][0]))
            restore_pic_list = restore_pic_list[:-1]
        elif len(restore_pic_list)==1:
            os.system('mv {} {}'.format(restore_pic_list[0][1],restore_pic_list[0][0]))
            restore_pic_list =[]
        else:
            print('被删除的图片都已恢复！')
        print(restore_pic_list)
    else:
        idx += 1
        

cv2.destroyAllWindows()

