import imagesize
import os
import sys
sys.path.append('..')
import utils

with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/imgsize.txt','a+') as f:
    for root,files in utils.walk('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/00_dataset/TSR/rename_3840x2160'):
        for file_ in files:
            width,height = imagesize.get(file_)
            comment = file_ + '|' +  str(width) +'x' + str(height) + '\n'
            # print(comment)
            f.write(comment)
        