import os
import argparse
import glob
from pathlib import Path
import re
import os.path as osp
import utils

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirpath', type=str)

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    sum1 = 0
    
    for root, files in utils.walk(args.dirpath):
        if len(files)==0:
            continue
        sum1 = sum1 + len(files)
        print(root, len(files))
    print(sum1)
