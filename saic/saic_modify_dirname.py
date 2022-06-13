# coding:utf-8
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--srcdir', type=str, required=True)
args = parser.parse_args()

src =  args.srcdir

#修改文件夹目录名称为TDA4需要的格式
for root, dirs, files in os.walk(src):
    for dir_ in dirs:
        if 'FrontLeft' in dir_:
            a = dir_.split('_')[0]
            os.system('mv {}/{} {}/{}-side_left_front'.format(root,dir_,root,a))
        if 'FrontRight' in dir_:
            a = dir_.split('_')[0]
            os.system('mv {}/{} {}/{}-side_right_front'.format(root,dir_,root,a))
        if 'RearLeft' in dir_:
            a = dir_.split('_')[0]
            os.system('mv {}/{} {}/{}-side_left_rear'.format(root,dir_,root,a))
        if 'RearRight' in dir_:
            a = dir_.split('_')[0]
            os.system('mv {}/{} {}/{}-side_right_rear'.format(root,dir_,root,a))
