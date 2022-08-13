import sys
sys.path.append('..')
import utils
import os


src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/3d_interlable'

for root,_,files in os.walk(src):
    for file_ in files:
        if 'FOV30' in root:
            newfilename = file_.replace('vc1','vc2')
        if 'FOV120' in root:
            newfilename = file_.replace('vc2','vc1')
        os.system('mv {} {}'.format(os.path.join(root,file_),os.path.join(root,newfilename)))
