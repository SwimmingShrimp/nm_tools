import os

img120 = '/data1/NMtest/DataChoice/NullMax/20220405/fov120'
img30 = '/data1/NMtest/DataChoice/NullMax/20220405/fov30'
img30_src = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_30'

for root,_,files in os.walk(img120):
    for file_ in files:
        if '_del' in root:
            continue
        filename = file_.replace('vc2','vc1')
        img120_file = os.path.join(root,filename)
        img30_file = root.replace(img120,img30)
        img30_src_file = img120_file.replace(img120,img30_src)
        if not os.path.exists(img30_file):
            os.makedirs(img30_file)
        command = 'cp {} {}'.format(img30_src_file,img30_file)
        os.system(command)
        print(command)
