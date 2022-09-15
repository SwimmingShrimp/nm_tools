import os
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('end',type=str)
# args = parser.parse_args()

# src120 = '/data/Unlabeled/testset/NullMax/FrontCam/fov_30/2022-01-27/2022-01-27-13-33/oimg'
# src30 = '/data/Unlabeled/testset/NullMax/FrontCam/fov_30/2022-01-27/2022-01-27-13-33/oimg'
# idx_end = int(args.end)
# idx_start = idx_end-14
# dst = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori/2022-01-27-13-33/case81'

# for root, dirs ,files in os.walk(src120):
#     for file_ in files:
#         filenamenum = int(file_[10:-4])
#         dst120 = os.path.join(dst,'FOV120')
#         os.makedirs(dst120,exist_ok=True)
#         if idx_start<=filenamenum <= idx_end:
#             os.system('cp {}/{} {}/{}'.format(root,file_,dst120,file_))
# for root, dirs ,files in os.walk(src30):
#     for file_ in files:
#         filenamenum = int(file_[10:-4])
#         dst30 = os.path.join(dst,'FOV30')
#         os.makedirs(dst30,exist_ok=True)
#         if idx_start<=filenamenum <= idx_end:
#             os.system('cp {}/{} {}/{}'.format(root,file_,dst30,file_))

idx_list =[780,1551,4756,8100,8822,9599,9878,10306,13408,15680,16479,20412,23814,24928,25749,26809,28775,28899,29781,30608,30662,31086,31724]

src120 = '/data/Unlabeled/trainset/NullMax/FrontCam/fov_120/2022-07-20/2022-07-20-11-35/video/2022-07-20-11-35'
src30 = '/data/Unlabeled/trainset/NullMax/FrontCam/fov_30/2022-07-20/2022-07-20-11-35/video/2022-07-20-11-35'
dst_dir = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori/2022-07-20-11-35'
# idx_end = int(args.end)

i = 1
for idx_end in idx_list:
    idx_end = int(idx_end)
    idx_start = idx_end-14
    dst = os.path.join(dst_dir,('case'+str(i)))
    for root, dirs ,files in os.walk(src120):
        for file_ in files:
            filenamenum = int(file_[:-4])
            dst120 = os.path.join(dst,'FOV120')
            os.makedirs(dst120,exist_ok=True)
            if idx_start<=filenamenum <= idx_end:
                os.system('cp {}/{} {}/{}'.format(root,file_,dst120,file_))
    for root, dirs ,files in os.walk(src30):
        for file_ in files:
            filenamenum = int(file_[:-4])
            dst30 = os.path.join(dst,'FOV30')
            os.makedirs(dst30,exist_ok=True)
            if idx_start<=filenamenum <= idx_end:
                os.system('cp {}/{} {}/{}'.format(root,file_,dst30,file_))
    i+=1

