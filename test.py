import sys
sys.path.append('..')
import utils
import os


src = '/media/lixialin/boot/lixialin/data2/front_3d_1920x1280_yuv_599/front_near'
for root, files in utils.walk(src):
    for file_ in files:
        num = os.path.basename(file_).split('_')[-1].split('.')[0]
        print(num)
        if int(num)<10:
            newfile= 'frame_vc1_0' + num + '.yuv'
            os.system('mv {} {}/{}'.format(file_,root,newfile))

# src = '/home/lixialin/Pictures/2/FOV30'
# for root,_ ,files in os.walk(src):
#     for file_ in files:
#         newfile = file_.replace('vc1','vc2')
#         os.system('mv {}/{} {}/{}'.format(root,file_,root,newfile))