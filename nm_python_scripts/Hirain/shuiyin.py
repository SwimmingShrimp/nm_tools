from watermarker.marker import add_mark
import argparse
import os
from PIL import Image

parser = argparse.ArgumentParser()

parser.add_argument('imgroot', help='img root',default=None, type=str)
args = parser.parse_args()

img = []

for (rt, dr, files) in os.walk(args.imgroot):
        if files != []:
            for item in files:
                if item.endswith('png') or item.endswith('bmp'):
                    img.append(os.path.join(rt, item))

for path in img:
    
    dir_name = os.path.dirname(os.path.abspath(path).replace("benchmark_ori_pic", "benchmark_ori_pic_watermark"))
    if os.path.exists(dir_name):
        pass
    else:
        os.makedirs(dir_name)
    newFileName = os.path.join(dir_name,os.path.basename(path)[:-4]+'.jpg')
    im = Image.open(path)
    im.save(newFileName)
    add_mark(file=newFileName, out=dir_name, mark="nullmax confidential", color= (123,123,123),opacity=0.3, angle=45, space=30)