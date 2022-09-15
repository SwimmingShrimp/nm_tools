import os
import re
import argparse
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils

src = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori'
dst = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/merge'
relation_src = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori'

idx = 600

with open('{}/relation.txt'.format(relation_src),'a+') as f:
    for root,files in utils.walk(src):
        if len(files)==0:
            continue
        if 'bak' in root:
            continue
        if 'FOV30' in root:     
            for file_ in files:
                if idx<10:
                    filerename = 'frame_vc2_0' + str(idx) + '.png'
                else:
                    filerename = 'frame_vc2_' + str(idx) + '.png'
                comment1 = file_ + '|' + filerename + '\n'
                commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
                os.system(commond1)
                f.write(comment1)
                idx +=1
    