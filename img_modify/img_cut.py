'''
原图1920X1280
本次版本裁切方案：上面裁切120，下面裁切200
operation_time:20220219
'''

import os
import cv2
import glob
from pathlib import Path
import re

src = '/media/lixialin/lxl/0_temp/data/2022-01-12-14-54/0_10000/5001-10000/FOV120_dist'
dst = '/media/lixialin/lxl/0_temp/data/2022-01-12-14-54/0_10000/5001-10000/FOV120_dist'

imgtypes = ['.jpg', '.bmp', '.png', '.yuv']
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

for root, files in walk(src):
    for file_ in files:
        print(file_)
        img = cv2.imread(file_)
        # y*x
        img_crop = img[200:1280,0:1920]
        # dst_file = file_.replace(src,dst)
        # dst_path = os.path.dirname(dst_file)       
        # print(dst_path)
        # if not os.path.exists(dst_path):
        #     os.makedirs(dst_path)
        # print(dst_file)
        cv2.imwrite(file_, img_crop,)




        

