import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start',type=str)
parser.add_argument('end',type=str)
args = parser.parse_args()

src = '/home/NULLMAX/lixialin/文档/project/preception_front/obstacle_perception/build_infer/x86_linux/image_record/image_record_pic/MosaicRes'
idx_start = int(args.start)
idx_end = int(args.end)
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/jira/FAULT-1283/output/case6'

for root, dirs ,files in os.walk(src):
    for file_ in files:
        filenamenum = int(file_[:-4])
        os.makedirs(dst,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst,file_))
