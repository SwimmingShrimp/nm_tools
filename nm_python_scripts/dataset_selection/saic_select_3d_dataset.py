import os
import cv2
import glob
from pathlib import Path
import re


imgpath = 'E:/new_3d_dataset/ori_data/ori_pic/2022-01-07-11-06'
dstpath = 'C:/Users/李夏临/Desktop/case6/image'
pcdsrc = 'E:/new_3d_dataset/ori_data/pcd/20220107-11-06-00'
pcddst = 'C:/Users/李夏临/Desktop/case6/pcd'

imgsrc = imgpath + '/0000-SideFrontLeft'
imgsrc2 = imgsrc.replace('SideFrontLeft','SideFrontRight')
imgsrc3 = imgsrc.replace('SideFrontLeft','SideRearRight')
imgsrc4 = imgsrc.replace('SideFrontLeft','SideRearLeft')
pcd_start_idx = 1641524964955
idx_num = 110*100

imgtypes = ['.jpg', '.bmp', '.png', '.yuv','.pcd']
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
    # assert(len(fpaths)), 'No images in p: {}'.format(p)
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

def get_img_list(pcd_filename,img_src):
    camera_files = []    
    for pcd_file_name in pcd_filename:
        for _, files in walk(img_src):
            for file_ in files:
                filename = int((os.path.basename(file_))[:-4])
                if pcd_file_name + 100 > filename > pcd_file_name:
                    camera_files.append(file_)
    return camera_files

def cp_camera_file(imgpath,dstpath,img_src,camera_files):
    camera_dst = img_src.replace(imgpath,dstpath)
    if not os.path.exists(camera_dst):
        os.makedirs(camera_dst)
    for temp in camera_files:
        command = 'cp {} {}'.format(temp,camera_dst)
        os.system(command)

def del_which_file(pcd_file_name,files_list,camera):
    is_exist_value = False
    del_file = None
    for file_ in files_list:
        file_name = (os.path.basename(file_))[:-4]
        if pcd_file_name <int(file_name) < pcd_file_name+100:            
            is_exist_value = True
            del_file = dstpath + '/' + camera + '/' + file_name + '.png'
    return del_file,is_exist_value

pcd_filename = []
pcd_files = []
for root, files in walk(pcdsrc):
    for file_ in files:
        filename = int((os.path.basename(file_))[:-4])
        if pcd_start_idx + idx_num >= filename >= pcd_start_idx:
            pcd_files.append(file_)
            pcd_filename.append(filename)
            if not os.path.exists(pcddst):
                os.makedirs(pcddst)
            command = 'cp {} {}'.format(file_,pcddst)
            os.system(command)

left_front_files = get_img_list(pcd_filename,imgsrc)
right_front_files = get_img_list(pcd_filename,imgsrc2)
right_rear_files = get_img_list(pcd_filename,imgsrc3)
left_rear_files = get_img_list(pcd_filename,imgsrc4)

cp_camera_file(imgpath,dstpath,imgsrc,left_front_files)
cp_camera_file(imgpath,dstpath,imgsrc2,right_front_files)
cp_camera_file(imgpath,dstpath,imgsrc3,right_rear_files)
cp_camera_file(imgpath,dstpath,imgsrc4,left_rear_files)

pcd_all_files = os.listdir(pcddst)
for pcd_file in pcd_all_files:
    pcd_file_name = int(pcd_file[:-4])
    del_pcd_file = pcddst + '/' + pcd_file
    print(del_pcd_file)
    del_left_front_file,left_front_value = del_which_file(pcd_file_name,left_front_files,'0000-SideFrontLeft')
    del_left_rear_file,left_rear_value = del_which_file(pcd_file_name,left_rear_files,'0000-SideRearLeft')
    del_right_front_file,right_front_value = del_which_file(pcd_file_name,right_front_files,'0000-SideFrontRight')
    del_right_rear_file,right_rear_value = del_which_file(pcd_file_name,right_rear_files,'0000-SideRearRight')
    
    if left_front_value==True and left_rear_value == True and right_front_value == True and right_rear_value == True:
        continue
    else:
        command_rm1 = 'rm {}'.format(del_left_front_file)
        command_rm2 = 'rm {}'.format(del_left_rear_file)
        command_rm3 = 'rm {}'.format(del_right_front_file)
        command_rm4 = 'rm {}'.format(del_right_rear_file)
        command_rm5 = 'rm {}'.format(del_pcd_file)
        print(command_rm1)
        if del_left_front_file!=None:
            os.system(command_rm1)
        if del_left_rear_file!=None:
            os.system(command_rm2)
        if del_right_front_file!=None:
            os.system(command_rm3)
        if del_right_rear_file!=None:
            os.system(command_rm4)
        os.system(command_rm5)
