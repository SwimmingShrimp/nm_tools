import os
import re
import argparse
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/3d_pic_deal/city/images_ud'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/3d_img/city'
relation_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/3d_pic'

idx1 = 0
idx2 = 0

with open('{}/relation.txt'.format(relation_src),'a+') as f:
    for root,files in utils.walk(src):
        if len(files)==0:
            continue
        if 'bak' in root:
            continue
        if 'FOV30' in root:     
            for file_ in files:
                if idx1<10:
                    filerename = 'frame_vc2_0' + str(idx1) + '.png'
                else:
                    filerename = 'frame_vc2_' + str(idx1) + '.png'
                comment1 = file_ + '|' + filerename + '\n'
                commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
                os.system(commond1)
                f.write(comment1)
                idx1 +=1
        elif 'FOV120' in root:     
            for file_ in files:
                if idx2<10:
                    filerename = 'frame_vc1_0' + str(idx2) + '.png'
                else:
                    filerename = 'frame_vc1_' + str(idx2) + '.png'
                comment1 = file_ + '|' + filerename + '\n'
                commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
                os.system(commond1)
                f.write(comment1)
                idx2 +=1
    