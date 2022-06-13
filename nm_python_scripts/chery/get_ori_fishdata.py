import os

src = '/data1/Unlabeled/trainset/NullMax/FishCam/fov_180/2021-12-22/2021-12-22-15-01'
dst = '/data1/NMtest/temp'

for root, dirs, files in os.walk(src):
    if 'config' in root:
        continue
    for file_ in files:
        dst_file = root.replace(src,dst)
        if not os.path.exists(dst_file):
            os.makedirs(dst_file)
        if 'vc9' in file_:
            filenum = int(file_[10:-4])
            print(filenum)
            if 200<=filenum<=600:
                os.system('cp {}/{} {}/{}'.format(root,file_,dst_file,file_))
        else:
            filenum = int(file_[11:-4])
            print(filenum)
            if 200<=filenum<=600:
                os.system('cp {}/{} {}/{}'.format(root,file_,dst_file,file_))
