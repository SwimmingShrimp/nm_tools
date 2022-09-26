import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('start',type=str)
parser.add_argument('end',type=str)
args = parser.parse_args()

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/result/image_record_1/image_record_pic/camera_fusion'
idx_start = int(args.start)
idx_end = int(args.end)
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/jira/FAULT-1715/output/case1'

for root, dirs ,files in os.walk(src):
    for file_ in files:
        filenamenum = int(file_[:-4])
        os.makedirs(dst,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst,file_))

src120 = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/2022-01-25/2022-01-25-09-50/oimg'
src30 = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_30/2022-01-25/2022-01-25-09-50/oimg'

for root, dirs ,files in os.walk(src120):
    for file_ in files:
        filenamenum = int(file_[10:-4])
        dst120 = os.path.join(dst,'FOV120')
        os.makedirs(dst120,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst120,file_))
for root, dirs ,files in os.walk(src30):
    for file_ in files:
        filenamenum = int(file_[10:-4])
        dst30 = os.path.join(dst,'FOV30')
        os.makedirs(dst30,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst30,file_))