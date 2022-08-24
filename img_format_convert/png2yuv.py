import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('pngpath', type=str,help='the position of the png picture')
parser.add_argument('yuvpath',type=str,help='the position of the generated yuv picture')
parser.add_argument('resolution',type=str,help='the resolution of the pic')
args = parser.parse_args()

pngpath = args.pngpath
yuvpath = args.yuvpath
resolution = args.resolution

for root, dirs, files in os.walk(pngpath):
    for file_ in files:
        if 'time' in file_:
            continue
        filename = file_.replace('bmp','yuv')
        real_dst = root.replace(pngpath,yuvpath)
        if not os.path.exists(real_dst):
            os.makedirs(real_dst)
        command = 'ffmpeg -s {} -pix_fmt nv12 -i {}/{} {}/{}'.format(resolution,root,file_,real_dst,filename)
        print(command)
        os.system(command)

