'''yuv to png/bmp'''
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('yuvpath', type=str,help='the position of the yuv picture')
parser.add_argument('imgpath',type=str,help='the position of the generated bmp/png picture')
parser.add_argument('img_suffix',type=str,help='the generated picture format:png/bmp')
parser.add_argument('resolution',type=str,help='the resolution of the pic')
args = parser.parse_args()

yuvpath = args.yuvpath
imgpath = args.imgpath
img_suffix = args.img_suffix
resolution = args.resolution

for root, dirs, files in os.walk(yuvpath):
    for file_ in files:
        if img_suffix == 'bmp':
            filename = file_.replace('yuv','bmp')
        elif img_suffix == 'png':
            filename = file_.replace('yuv','png')
        real_dst = root.replace(yuvpath,imgpath)
        if not os.path.exists(real_dst):
            os.makedirs(real_dst)
        if img_suffix == 'bmp':
            command = "ffmpeg -s {} -pix_fmt nv12 -i {}/{} -pix_fmt rgb24 {}/{}".format(resolution,root,file_,real_dst,filename)
        elif img_suffix == 'png':
            command = "ffmpeg -s {} -pix_fmt nv12 -i {}/{} -vframes 1 -compression_level 5 {}/{}".format(resolution,root,file_,real_dst,filename)
        print(command)
        os.system(command)

