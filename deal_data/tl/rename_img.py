import os
import re
import argparse
import glob
from pathlib import Path
import re
import sys
sys.path.append('..')
import utils
import imagesize

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/3840x2160_jpg'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/3840x2160_jpg_rename'
relation_txt = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TL/traffic_light_benchmark/relation.txt'
os.makedirs(dst,exist_ok=True)

idx = 0
with open(relation_txt,'a+') as f:
    for root,files in utils.walk(src):
        for file_ in files:
            filerename = str(idx) + '.jpg'
            # if file_.endswith('.bmp'):
            #     filerename = str(idx) + '.bmp'
            # elif file_.endswith('.png'):
            #     filerename = str(idx) + '.png'
            # elif file_.endswith('.jpg'):
            #     filerename = str(idx) + '.jpg'
            width,height = imagesize.get(file_)
            comment1 = file_ + '|' + filerename +  '|' +  str(width) +'x' + str(height) +  '\n'
            commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
            os.system(commond1)
            # f.write(comment1)
            idx +=1