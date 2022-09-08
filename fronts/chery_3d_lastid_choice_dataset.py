import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('end',type=str)
args = parser.parse_args()

src120 = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/2022-01-12/2022-01-12-14-54/oimg'
src30 = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_30/2022-01-12/2022-01-12-14-54/oimg'
idx_end = int(args.end)
idx_start = idx_end-14
dst = '/data1/NMtest/others/DataChoice/NullMax/3D/ori_2022-01-12-14-54/case40'

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
