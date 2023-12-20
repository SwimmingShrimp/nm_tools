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
        filename = file_.replace('png','bmp')
        # filename = filename.replace('vc2','vc1')
        real_dst = root.replace(pngpath,yuvpath)
        if not os.path.exists(real_dst):
            os.makedirs(real_dst)
        command = 'ffmpeg -i {}/{} -s {} -pix_fmt bgr24 {}/{}'.format(root,file_,resolution,real_dst,filename)
        print(command)
        os.system(command)

