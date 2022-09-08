import sys
sys.path.append("..")
import utils
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src', type=str,help='the position of the src picture')
parser.add_argument('dst', type=str,help='the position of the dst picture')
args = parser.parse_args()

src = args.src
dst = args.dst

idx1,idx2 = 0,0

dst1 = os.path.join(dst,'FOV30')
dst2 = os.path.join(dst,'FOV120')
os.makedirs(dst1,exist_ok=True)
os.makedirs(dst2,exist_ok=True)
for root,files in utils.walk(src):
    for file_ in files:
        filename = os.path.basename(file_)
        if 'FOV30' in root:
            if idx1<10:
                file_dst = 'frame_vc2_0' + str(idx1) + '.png'
            else:
                file_dst = 'frame_vc2_' + str(idx1) + '.png'
            os.system('cp {} {}/{}'.format(file_,dst1,file_dst))
            idx1+=1
        else:
            if idx1<10:
                file_dst = 'frame_vc1_0' + str(idx2) + '.png'
            else:
                file_dst = 'frame_vc1_' + str(idx2) + '.png'
            os.system('cp {} {}/{}'.format(file_,dst2,file_dst))
            idx2+=1
