import os
import re
import argparse
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/ADB_IHC/IMAGE/benchmark_adb/monight'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/ADB_IHC/pic_rename/monight'
relation_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/ADB_IHC'

idx1 = 0
idx2 = 0

with open('{}/relation_night.txt'.format(relation_src),'a+') as f:
    for root,files in utils.walk(src):
        # real_dst = root.replace(src,dst)
        os.makedirs(dst,exist_ok=True)
        # if 'oimg' in root:     
        for file_ in files:
                # if idx1<10:
                #     filerename = 'frame_vc2_0' + str(idx1) + '.png'
                # else:
                    # filerename = 'frame_vc2_' + str(idx1) + '.png'
            if file_.endswith('.bmp'):
                filerename = str(idx1) + '.bmp'
            elif file_.endswith('.png'):
                filerename = str(idx1) + '.png'
            comment1 = file_ + '|' + filerename + '\n'
            commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
            os.system(commond1)
            f.write(comment1)
            idx1 +=1
        # elif 'FOV120' in root:     
        #     for file_ in files:
        #         if idx2<10:
        #             filerename = 'frame_vc1_0' + str(idx2) + '.png'
        #         else:
        #             filerename = 'frame_vc1_' + str(idx2) + '.png'
        #         comment1 = file_ + '|' + filerename + '\n'
        #         commond1 = 'cp {} {}/{}'.format(file_,real_dst,filerename)
        #         os.system(commond1)
        #         f.write(comment1)
        #         idx2 +=1
    