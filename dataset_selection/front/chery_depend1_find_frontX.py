import os
import sys
sys.path.append('..')
import utils


img1 = '/data/NMtest/others/DataChoice/NullMax/2D/batch2/2D_batch2_ori_1/2021-12-14-15-37'
imgfrontX = '/data/NMtest/others/DataChoice/NullMax/2D/batch2/2D_batch2_ori_30/2021-12-14-15-37'
img_src = '/data/Unlabeled/testset/NullMax/FrontCam/fov_30/'

for root,files in utils.walk(img1):
    for file_ in files:
        if 'FOV30' in root and 'FOV120' not in root:
            filenum = int(os.path.basename(file_).split('.')[0].split('_')[-1])
            print(filenum)
            for i in range(30):
                filenewnum = filenum-i
                if filenewnum<0:
                    break
                filenewname = 'frame_vc1_' + str(filenewnum) + '.png'
                date_hour = root.split('/')[-2]
                date_day = date_hour.rsplit('-',2)[0]
                new_imgpath = os.path.join(img_src,date_day,date_hour,'oimg')
                # imgpath_cp1 = os.path.join(new_imgpath,date_hour)
                # imgpath_cp2 = os.path.join(new_imgpath,(date_hour+'_'))
                # pathvalue = os.path.isdir(imgpath_cp1)
                # if pathvalue:
                #     src_cp = imgpath_cp1
                # else:
                #     src_cp = imgpath_cp2
                src_cp = new_imgpath
                dst_src = root.replace(img1,imgfrontX)                
                os.makedirs(dst_src,exist_ok=True)
                command ='cp {}/{} {}'.format(src_cp,filenewname,dst_src)
                print(command)
                os.system(command)


