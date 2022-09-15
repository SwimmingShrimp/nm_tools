import os
import sys
sys.path.append("..")
import utils

img_path = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori'
pcd_path1 = '/data/Unlabeled/testset/NullMax/FrontCam/fov_120'
pcd_path2 = '/data/Unlabeled/trainset/NullMax/FrontCam/fov_120'
pcd_file = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori/pcd.txt'
relation_txtfile = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/ori/relation.txt'
pcd_dst = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/merge/lable/pcd'
lable_path ='/data/NMtest/others/DataChoice/NullMax/3D/batch2/merge/lable/FOV30'

def get_lable_list():
    for root,_,files in os.walk(lable_path):
        pass
    return files
        
def depend_inttime_get_pcdname(new_pcd_path,int_time):
    mindiff = 1000000
    pcdname = '1.pcd'
    for root,files in utils.walk(new_pcd_path):
        for file_ in files:
            filename = os.path.basename(file_)
            filenum1 = int(filename.rsplit('.')[0])
            filenum2 = int(filename.rsplit('.')[1])
            filenum = int((filenum1)*1000000 + filenum2/1000)
            if mindiff>abs(filenum-int_time):
                mindiff = abs(filenum-int_time)
                pcdname = filename
    print(pcdname)
    return pcdname


def get_newfile_name(file_):
    with open(relation_txtfile,'r') as f1:
        for line in f1.readlines():
            oldfile = line.split("|")[0]
            if file_ == oldfile:
                newfilename =line.split("|")[-1][:-1]
                return newfilename

def get_timestamp(filenum,timestamp):
    with open(timestamp,'r') as f:
        for timestamp_line in f.readlines():
            frameid = timestamp_line.split(' ')[-1]
            if int(frameid) == int(filenum):
                int_time = int(timestamp_line.split(' ')[-4])
    return int_time


def get_pcd_txt():
    with open(pcd_file,'a+') as f:
        for root,files in utils.walk(img_path):
            for file_ in files:
                if 'FOV30' in root and 'bak' not in root:
                    # 获取重命名后的文件名称
                    new_file_name = get_newfile_name(file_)
                    num = int(new_file_name.split('.')[0].split('_')[-1])

                    # 获取标注的文件列表
                    lable_file_list = get_lable_list() 

                    if new_file_name in lable_file_list and num>0:
                        #根据新frame_id的名称移动pcd
                        print(new_file_name)

                        hour = file_.split('/')[-4]
                        day = hour.rsplit('-',2)[0]
                        filenum = os.path.basename(file_).split('.')[0]
                        new_pcd_path1 = os.path.join(pcd_path1,day,hour)
                        new_pcd_path2 = os.path.join(pcd_path2,day,hour)
                        if os.path.isdir(new_pcd_path1):
                            new_pcd_path_real=new_pcd_path1
                        else:
                            new_pcd_path_real=new_pcd_path2
                        new_pcd_path = os.path.join(new_pcd_path_real,'config/pcd')
                        timestamp = os.path.join(new_pcd_path_real,'config','timestamp_vc2.log')
                        # 根据frame_id获取时间戳
                        int_time = get_timestamp(filenum,timestamp)

                        # 根据时间戳获取pcd的名称
                        pcd_name = depend_inttime_get_pcdname(new_pcd_path,int_time)
                        newpcdname = new_file_name.replace('png','pcd')        

                        #将对应存入到txt文档中
                        comment = file_ + '|' + new_file_name + '|' + os.path.join(new_pcd_path,pcd_name) + '|' + newpcdname + '\n'
                        print(comment)
                        f.write(comment)

def mv_pcd_file():
    with open(pcd_file,'r') as f:
        for line in f.readlines():
            # print(line)
            old_pcdfile = line.split('|')[-2]
            new_pcdfile = line.split('|')[-1]
            os.makedirs(pcd_dst,exist_ok=True)
            new_pcdfile = os.path.join(pcd_dst,new_pcdfile)
            command = 'cp {} {}'.format(old_pcdfile,new_pcdfile)
            print(command)
            os.system(command)

def main():
    # get_pcd_txt()
    mv_pcd_file()
                
if __name__=='__main__':
    main()           
            

