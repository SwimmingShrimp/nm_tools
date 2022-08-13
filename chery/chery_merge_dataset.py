import sys
sys.path.append("..")
import utils
import os

src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/640x384_bmp'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/640x384_rename_bmp/FOV30'
txtfile = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/data/relation.txt'

idx = 0
os.makedirs(dst,exist_ok=True)
with open(txtfile,'a+') as f:
    for root, files in utils.walk(src):
        for file_ in files:
            new_filename = 'frame_vc2_' + str(idx) + '.bmp'
            command = 'cp {} {}/{}'.format(file_ ,dst,new_filename)
            print(command)
            os.system(command)
            idx +=1
            comment = file_ + '|' + new_filename + '\n'
            print(comment)
            f.write(comment)