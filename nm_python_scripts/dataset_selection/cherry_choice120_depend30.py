import os

img120 = '/data1/NMtest/others/DataChoice/NullMax/Lane/2022-02-07/2022-02-07_ori_1/FOV120'
img30 = '/data1/NMtest/others/DataChoice/NullMax/Lane/2022-02-07/2022-02-07_ori_1/FOV30'
img120_src = '/data1/Unlabeled/trainset/NullMax/FrontCam/fov_120/2022-02-07'

for root,_,files in os.walk(img30):
    for file_ in files:
        if 'oimg' in root:
            img120_path = root.replace(img30,img120)
            img120_src_path = root.replace(img30,img120_src)
            if not os.path.exists(img120_path):
                os.makedirs(img120_path)
            img120_src_file = file_.replace('vc1','vc2')
            command = 'cp {}/{} {}'.format(img120_src_path,img120_src_file,img120_path)
            os.system(command)
            print(command)
