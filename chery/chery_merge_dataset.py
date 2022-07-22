import sys
sys.path.append("..")
import utils
import os

src = '/data1/NMtest/others/DataChoice/NullMax/3D/ori_2022-01-12-14-54'
dst = '/data1/NMtest/others/DataChoice/NullMax/3D/merge_2022-01-12-14-54/FOV120'
txtfile = '/data1/NMtest/others/DataChoice/NullMax/3D/ori_2022-01-12-14-54/relation.txt'

idx = 0
os.makedirs(dst,exist_ok=True)
with open(txtfile,'a+') as f:
    for root, files in utils.walk(src):
        for file_ in files:
            if 'FOV120' in root:
                new_filename = 'frame_vc1_' + str(idx) + '.png'
                command = 'cp {} {}/{}'.format(file_ ,dst,new_filename)
                print(command)
                os.system(command)
                idx +=1
                comment = file_ + '|' + new_filename + '\n'
                print(comment)
                # f.write(comment)