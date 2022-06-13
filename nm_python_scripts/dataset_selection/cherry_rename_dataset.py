import os
import re
import argparse
import glob
from pathlib import Path
import re
import os.path as osp


src = '/data1/NMtest/others/DataChoice/NullMax/Lane/2021-12-14/2021-12-14_undist_1/FOV120'
dst = '/data1/NMtest/others/DataChoice/NullMax/Lane/Dataset/day/front_near'
relation_src = '/data1/NMtest/others/DataChoice/NullMax/Lane/Dataset/day'

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

idx = 1381

with open('{}/relation.txt'.format(relation_src),'a+') as f:
    for root,files in walk(src):
        if len(files)==0:
            continue       
        for file_ in files:
            # 120°是vc2
            if idx<10:
                filerename = 'frame_vc2_0' + str(idx) + '.png'
            else:
                filerename = 'frame_vc2_' + str(idx) + '.png'
            comment1 = file_ + '|' + filerename + '\n'
            commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
            os.system(commond1)
            f.write(comment1)
            idx +=1
            # 30°是vc1
            # if idx > 39902:
            #     continue
            # if idx<10:
            #     filerename2 = 'frame_vc1_0' + str(idx) + '.png'
            # else:
            #     filerename2 = 'frame_vc1_' + str(idx) + '.png'
            # comment2 = file_ + '|' + filerename2 + '\n'
            # commond2 = 'cp {} {}/{}'.format(file_,dst,filerename2)
            # os.system(commond2)
            # f.write(comment2)
            # idx +=1