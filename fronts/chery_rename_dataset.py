import os
import re
import argparse
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils

src = '/data1/NMtest/others/DataChoice/NullMax/Lane/2021-12-14/2021-12-14_undist_1/FOV120'
dst = '/data1/NMtest/others/DataChoice/NullMax/Lane/Dataset/day/front_near'
relation_src = '/data1/NMtest/others/DataChoice/NullMax/Lane/Dataset/day'

idx = 1381

with open('{}/relation.txt'.format(relation_src),'a+') as f:
    for root,files in utils.walk(src):
        if len(files)==0:
            continue       
        for file_ in files:
            # 120°是vc1
            if idx<10:
                filerename = 'frame_vc2_0' + str(idx) + '.png'
            else:
                filerename = 'frame_vc2_' + str(idx) + '.png'
            comment1 = file_ + '|' + filerename + '\n'
            commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
            os.system(commond1)
            f.write(comment1)
            idx +=1
            # 30°是vc2
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