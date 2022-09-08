import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('yuvpath', type=str,help='the position of the yuv picture')
args = parser.parse_args()

yuvpath = args.yuvpath

for root, dirs, files in os.walk(yuvpath):
    for file_ in files:
        filenum = file_[10:-4]
        if int(filenum)<10:
            filenew = file_[:10] +'0' +filenum + '.yuv'
            command ='mv {}/{} {}/{}'.format(root,file_,root,filenew)
            print(command)
            os.system(command)

