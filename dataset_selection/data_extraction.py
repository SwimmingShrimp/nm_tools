# -*- coding:utf-8 -*-
import os
from pathlib import Path
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--src',type=str, required=True)
parser.add_argument('--dst',type=str, required=True)
args = parser.parse_args()

src = args.src
dst = args.dst

for root, _, files in os.walk(src):
    if len(files)<40:
        continue
    if 'oimg' in root:
        try:
            files = sorted(files, key=lambda fname: int(re.sub(r'[^0-9]', '', fname)))
        except:
            print(root, files)
        
        # print(files)
        for ind in range(1,len(files),150):
            if ind<10:
                continue
            fpath = dst / Path(root).relative_to(src)
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            # 把挑选出来的图片放到目标文件夹下
            os.system("cp {} {}".format(os.path.join(root, files[ind]), fpath))


