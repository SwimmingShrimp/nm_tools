import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('bmppath', type=str,help='the position of the bmp picture')
parser.add_argument('pngpath',type=str,help='the position of the generated yuv picture')
# parser.add_argument('resolution',type=str,help='the resolution of the pic')
args = parser.parse_args()

bmppath = args.bmppath
pngpath = args.pngpath
# resolution = args.resolution
if not os.path.exists(pngpath):
    os.makedirs(pngpath)
for root, dirs, files in os.walk(bmppath):
    for file_ in files:
        real_dst = root.replace(bmppath,pngpath) 
        if not os.path.exists(real_dst):
            os.makedirs(real_dst)
        # if file_.endswith('.bmp'):
        #     filename = file_.replace('bmp','png')
        # # filename = filename.replace('vc2','vc1')
        #                
        #     command = 'ffmpeg -i {} {}'.format(os.path.join(root,file_),os.path.join(real_dst,filename))
        #     print(command)
        #     os.system(command)
        if file_.endswith('.png'):
            
            os.system('cp {} {}'.format(os.path.join(root,file_),real_dst))
