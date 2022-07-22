src30 ='/data1/Unlabeled/trainset/NullMax/FrontCam/fov_30/2022-03-03/2022-03-03-14-30/oimg'
src120 = '/data1/Unlabeled/trainset/NullMax/FrontCam/fov_120/2022-03-03/2022-03-03-14-30/oimg'

for root, dirs ,files in os.walk(src):
    for file_ in files:
        filenamenum = int(file_[:-4])
        os.makedirs(dst,exist_ok=True)
        if idx_start<=filenamenum <= idx_end:
            os.system('cp {}/{} {}/{}'.format(root,file_,dst,file_))