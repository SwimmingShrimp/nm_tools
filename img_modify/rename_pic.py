import sys
sys.path.append("..")
import utils
import os

idx1,idx2 = 0,0
dst1 = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Qirui/TL/tl_1920x1280_png/FOV30'
dst2 = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Qirui/TL/tl_1920x1280_png/FOV120'
os.makedirs(dst1,exist_ok=True)
os.makedirs(dst2,exist_ok=True)
for root,files in utils.walk('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/DataSet/Qirui/TL/tl_1920x1080_png'):
    for file_ in files:
        filename = os.path.basename(file_)
        if 'FOV30' in root:
            if idx1<10:
                file_dst = 'frame_vc2_0' + str(idx1) + '.png'
            else:
                file_dst = 'frame_vc2_' + str(idx1) + '.png'
            os.system('cp {} {}/{}'.format(file_,dst1,file_dst))
            idx1+=1
        else:
            if idx1<10:
                file_dst = 'frame_vc1_0' + str(idx2) + '.png'
            else:
                file_dst = 'frame_vc1_' + str(idx2) + '.png'
            os.system('cp {} {}/{}'.format(file_,dst2,file_dst))
            idx2+=1
