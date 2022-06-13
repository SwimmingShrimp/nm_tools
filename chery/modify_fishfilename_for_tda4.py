import os
import re
import argparse
import glob
from pathlib import Path
import re
import os.path as osp


src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/data/cherry_fish_tda4/yuv'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/data/cherry_fish_tda4/yuv_rename'

#遍历文件下所有文件，返回函数walks： for root,files in walks(src):  files返回绝对路径+文件，且已从小到大排序
imgtypes = ['.jpg', '.bmp', '.png']
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

idx1,idx2,idx3,idx4 = 0,0,0,0


for root,files in walk(src):
    if len(files)==0:
        continue
    file_dst = root.replace(src,dst)
    if not os.path.exists(file_dst): 
        os.makedirs(file_dst)      
    for file_ in files:
        if 'fish_left' in root:
            filerename1 = 'frame_vc8_' + str(idx1) + '.bmp'
            commond1 = 'cp {} {}/{}'.format(file_,file_dst,filerename1)
            print(commond1)
            os.system(commond1)
            idx1 +=1
        if 'fish_front' in root:
            filerename2 = 'frame_vc9_' + str(idx2) + '.bmp'
            commond2 = 'cp {} {}/{}'.format(file_,file_dst,filerename2)
            os.system(commond2)
            idx2 +=1
        if 'fish_right' in root:
            filerename3 = 'frame_vc10_' + str(idx3) + '.bmp'
            commond3 = 'cp {} {}/{}'.format(file_,file_dst,filerename3)
            os.system(commond3)
            idx3 +=1
        if 'fish_back' in root:
            filerename4 = 'frame_vc11_' + str(idx4) + '.bmp'
            commond4 = 'cp {} {}/{}'.format(file_,file_dst,filerename4)
            os.system(commond4)
            idx4 +=1
