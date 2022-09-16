import os
import argparse
import sys
sys.path.append("..")
import utils

parser = argparse.ArgumentParser()
parser.add_argument('src',type=str)
parser.add_argument('dst',type=str)
args = parser.parse_args()

src = args.src
dst = args.dst

for root, files in utils.walk(src):
    for file_ in files:
        # num = os.path.basename(file_).split('_')[-1].split('.')[0]
        num = os.path.basename(file_).split('.')[0]
        if int(num)<10000:
            dst1 = os.path.join(dst,'1')
            os.makedirs(dst1,exist_ok=True)
            os.system('cp {} {}'.format(file_,dst1,))
        elif 10000<=int(num)<20000:
            dst2 = os.path.join(dst,'2')
            os.makedirs(dst2,exist_ok=True)
            os.system('cp {} {}'.format(file_,dst2,))
        elif 20000<=int(num)<30000:
            dst3 = os.path.join(dst,'3')
            os.makedirs(dst3,exist_ok=True)
            os.system('cp {} {}'.format(file_,dst3,))
        elif 30000<=int(num)<40000:
            dst4 = os.path.join(dst,'4')
            os.makedirs(dst4,exist_ok=True)
            os.system('cp {} {}'.format(file_,dst4,))
        elif 40000<=int(num)<50000:
            dst5 = os.path.join(dst,'5')
            os.makedirs(dst5,exist_ok=True)
            os.system('cp {} {}'.format(file_,dst5,))
