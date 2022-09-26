import utils
import os

idx =0 
src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/2022-01-12-14-54/1/FOV30'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/2022-01-12-14-54/1/FOV30'
relation_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/2D/new_night'

os.makedirs(dst,exist_ok=True)
idx = 0
with open('{}/relation_night.txt'.format(relation_src),'a+') as f:
    for root,files in utils.walk(src):
        # files.sort(key=lambda x:int(x.split('.')[0]))
        for file_ in files:
            if idx<10:
                filerename = 'frame_vc1_0' + str(idx) + '.png'
            else:
                filerename = 'frame_vc1_' + str(idx) + '.png'
            # comment1 = file_ + '|' + filerename + '\n'
            commond1 = 'cp {} {}/{}'.format(file_,dst,filerename)
            print(commond1)
            os.system(commond1)
            # f.write(comment1)
            idx +=1

