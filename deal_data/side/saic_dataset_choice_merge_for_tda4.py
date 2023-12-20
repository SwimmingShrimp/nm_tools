import os
import re
import argparse
import glob
from pathlib import Path
import re
import os.path as osp
import utils


parser = argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
args = parser.parse_args()

src = args.src
dst = args.dst
os.system('touch {}/relation.txt'.format(dst))
os.makedirs('{}/side_left_front'.format(dst))
os.makedirs('{}/side_left_rear'.format(dst))
os.makedirs('{}/side_right_front'.format(dst))
os.makedirs('{}/side_right_rear'.format(dst))
index1=0
index2=0
index3=0
index4=0
with open('{}/relation.txt'.format(dst),'a+') as f:
    for root,files in utils.walk(src):
        if len(files)==0:
            continue       
        if 'SideRearLeft' in root:
            for file_ in files:
                renamefile1 = 'frame_vc5_' + str(index1) + '.png'
                comment1 = file_ + '|' + renamefile1 + '\n'
                commond1 = 'cp {} {}/side_left_rear/{}'.format(file_,dst,renamefile1)
                os.system(commond1)
                f.write(comment1)
                index1 +=1
        elif 'SideFrontLeft' in root:
            for file_ in files:
                renamefile2 = 'frame_vc6_' + str(index2) + '.png'
                comment2 = file_ + '|' + renamefile2 + '\n'
                commond2 = 'cp {} {}/side_left_front/{}'.format(file_,dst,renamefile2)
                os.system(commond2)
                f.write(comment2)
                index2 +=1
        elif 'SideFrontRight' in root:
            for file_ in files:
                renamefile3 = 'frame_vc7_' + str(index3) + '.png'
                comment3 = file_ + '|' + renamefile3 + '\n'
                commond3 = 'cp {} {}/side_right_front/{}'.format(file_,dst,renamefile3)
                os.system(commond3)
                f.write(comment3)
                index3 +=1
        elif 'SideRearRight' in root:
            for file_ in files:
                renamefile4 = 'frame_vc8_' + str(index4) + '.png'
                comment4 = file_ + '|' + renamefile4 + '\n'
                commond4 = 'cp {} {}/side_right_rear/{}'.format(file_,dst,renamefile4)
                os.system(commond4)
                f.write(comment4)
                index4 +=1 
