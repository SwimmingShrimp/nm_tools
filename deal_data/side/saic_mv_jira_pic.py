import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('src',type=str)
parser.add_argument('cammera_pos',type=str)
parser.add_argument('start',type=str)
parser.add_argument('end',type=str)
parser.add_argument('dst',type=str)
args = parser.parse_args()

src = args.src
pos = args.cammera_pos
idx_start = args.start
idx_end = args.end
dst = args.dst

if '5' in pos:
    if not os.path.exists(dst + '/left_rear'):
        os.makedirs(dst + '/left_rear')
    for i in range(int(idx_start),int(idx_end)+1):
        j = str(i).zfill(4)
        command = 'cp {}/0001-SideRearLeft/{}.png {}/left_rear'.format(src,j,dst)
        print(command)
        os.system(command)
if '6' in pos:
    if not os.path.exists(dst + '/left_front'):
        os.makedirs(dst + '/left_front')
    for i in range(int(idx_start),int(idx_end)+1):
        j = str(i).zfill(4)
        command = 'cp {}/0001-SideFrontLeft/{}.png {}/left_front'.format(src,j,dst)
        print(command)
        os.system(command)
if '7' in pos:
    if not os.path.exists(dst + '/right_front'):
        os.makedirs(dst + '/right_front')
    for i in range(int(idx_start),int(idx_end)+1):
        j = str(i).zfill(4)
        command = 'cp {}/0001-SideFrontRight/{}.png {}/right_front'.format(src,j,dst)
        print(command)
        os.system(command)
if '8' in pos:
    if not os.path.exists(dst + '/right_rear'):
        os.makedirs(dst + '/right_rear')
    for i in range(int(idx_start),int(idx_end)+1):
        j = str(i).zfill(4)
        command = 'cp {}/0001-SideRearRight/{}.png {}/right_rear'.format(src,j,dst)
        print(command)
        os.system(command)
