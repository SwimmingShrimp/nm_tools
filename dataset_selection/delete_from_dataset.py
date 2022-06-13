import os
import json
import logging
import cv2
import re
import glob
from pathlib import Path

imgtypes = ['.jpg', '.bmp', '.png']
def usort(fnames):
    if isinstance(fnames, dict):
        fnames = dict(sorted(fnames.items(), key=lambda k: int(re.sub(r'[^0-9]', '', k[0]))))
    elif isinstance(fnames, list):
        if len(fnames) and re.sub(r'[^0-9]', '', fnames[0]) != '':
            if isinstance(fnames[0], list):
                fnames = sorted(fnames, key=lambda k:int(re.sub(r'[^0-9]', '', k[0])))
            elif isinstance(fnames[0], dict):
                fnames = dict(sorted(fnames.items(), key=lambda k:int(re.sub(r'[^0-9]', '', k))))
            else:
                # if 'Side' in fnames[0]:
                #     print(int(fnames[0].split('/')[-1].split('-')[1] + fnames[0].split('/')[-1].split('-')[1]))
                #     fnames = sorted(fnames, key=lambda fname:int(fname.split('/')[-1].split('-')[1] + fname.split('/')[-1].split('-')[0]))
                # else:
                fnames = sorted(fnames, key=lambda fname:int(re.sub(r'[^0-9]', '', fname)))
            return fnames
    else:
        pass
    return fnames
def walk(p, regex='**/*'):
    regex = '**/*' if regex == '*' else regex
    fpaths = glob.glob('{}/{}'.format(p, regex), recursive=True)
    fpaths = [fpath for fpath in fpaths if fpath[-4:] in imgtypes]
    # print('==> Number: {:<6d}, Path: {}'.format(len(fpaths), '{}/{}'.format(osp.abspath(p), regex)))
    assert(len(fpaths)), 'No images in p: {}'.format(p)
    if fpaths:
        walks = {}
        for fpath in fpaths:
            dirpath = Path(fpath).parent.as_posix()
            if dirpath not in walks:
                walks[dirpath] = [fpath]
            else:
                walks[dirpath].append(fpath)

        for dirpath, fpaths in walks.items():
            try:
                walks[dirpath] = usort(fpaths)
            except:
                walks[dirpath] = fpaths
        try:
            walks = usort(walks).items()
        except:
            print('    !!!Sort error!!!')
            walks = walks.items()
    return walks


img_src = '/data1/NMtest/CornerCaseAndPseudoGT/JIRA/chery_front_120_30_jira/FAULT-1339/input/case1/FOV30'

for root, files in walk(img_src):
    pass

cv2.namedWindow('ViewPic',cv2.WINDOW_NORMAL)
idx = 0
while True:
    img = cv2.imread(files[idx])
    print(files[idx])
    cv2.imshow('ViewPic',img)
    key = cv2.waitKey(0)
    if key == ord('q'):
        break
    elif key == ord('b'):
        idx -= 1
    elif key == ord('d'):
        os.system('rm {}'.format(files[idx]))
        print('the delete file name is ',files[idx])
        idx +=1
    elif key == ord('1'):
        idx +=100
    elif key == ord('2'):
        idx +=1000
    else:
        idx += 1
cv2.destroyAllWindows()


