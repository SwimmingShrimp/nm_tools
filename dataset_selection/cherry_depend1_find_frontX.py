import os

img1 = '/data1/NMtest/others/DataChoice/NullMax/2D/2D_batch1_ori_1/day/front_near'
imgfrontX = '/data1/NMtest/others/DataChoice/NullMax/2D/2D_batch1_ori_15/day/front_near'
img_src = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/'

for root,_,files in os.walk(img1):
    for file_ in files:
        if 'oimg' in root:
            filenum = int(file_[10:-4])
            print(filenum)
            for i in range(30):
                filenewnum = filenum-i
                filename = 'frame_vc2_' + str(filenewnum) + '.png'
                # cp_src = root.replace(img1,img_src)
                date = (root.split('/')[-2]).rsplit('-',2)[0]
                img_src_new = os.path.join(img_src,date)
                cp_src = root.replace(img1,img_src_new)
                # print(cp_src)
                dst_src = root.replace(img1,imgfrontX)
                if not os.path.exists(dst_src):
                    os.makedirs(dst_src)
                os.system('cp {}/{} {}'.format(cp_src,filename,dst_src))


