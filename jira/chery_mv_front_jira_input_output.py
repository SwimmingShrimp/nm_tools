import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start',type=str)
parser.add_argument('end',type=str)
args = parser.parse_args()

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/result/image_record_1/image_record_pic/camera_fusion'
idx_start = int(args.start)
idx_end = int(args.end)
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/jira/FAULT-1718/case2'

for root, dirs ,files in os.walk(src):
    for file_ in files:
        filenamenum = int(file_[:-4])
        dst_output = os.path.join(dst,'output')
        os.makedirs(dst_output,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst_output,file_))


src120 = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/2022-01-12-14-54/1/FOV120'
src30 = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/2022-01-12-14-54/1/FOV30'

for root, dirs ,files in os.walk(src120):
    for file_ in files:
        filenamenum = int(file_[10:-4])
        dst120 = os.path.join(dst,'input','FOV120')
        os.makedirs(dst120,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst120,file_))
for root, dirs ,files in os.walk(src30):
    for file_ in files:
        filenamenum = int(file_[10:-4])
        dst30 = os.path.join(dst,'input','FOV30')
        os.makedirs(dst30,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst30,file_))