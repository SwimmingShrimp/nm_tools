import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('pngpath', type=str,help='the position of the png picture')
parser.add_argument('jpgpath',type=str,help='the position of the generated yuv picture')
# parser.add_argument('resolution',type=str,help='the resolution of the pic')
args = parser.parse_args()

pngpath = args.pngpath
jpgpath = args.jpgpath
# resolution = args.resolution

for root, dirs, files in os.walk(pngpath):
    for file_ in files:
        filename = file_.replace('png','jpg')
        # filename = filename.replace('vc2','vc1')
        real_dst = root.replace(pngpath,jpgpath)
        if not os.path.exists(real_dst):
            os.makedirs(real_dst)
        command = 'ffmpeg -i {} {}'.format(os.path.join(root,file_),os.path.join(real_dst,filename))
        print(command)
        os.system(command)  

