import os
import sys
sys.path.append("..")
import utils

src = '/data1/NMtest/others/DataChoice/NullMax/3D/lable_2022-01-12-14-54/FOV30'
relation_txtfile = '/data1/NMtest/others/DataChoice/NullMax/3D/ori_2022-01-12-14-54/relation.txt'
timestamp_file = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/2022-01-12/2022-01-12-14-54/config/timestamp_vc2.log'
pcd_file = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/2022-01-12/2022-01-12-14-54/config/radar'
newpcd_filepath1 = '/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/ori'
newpcd_filepath2 = '/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/rename'
pcd_filetxt ='/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/pcd.txt'
if not os.path.exists(newpcd_filepath1): 
    os.makedirs(newpcd_filepath1)
if not os.path.exists(newpcd_filepath2): 
    os.makedirs(newpcd_filepath2)

'''获取pcd.txt'''
# src = '/data1/Unlabeled/testset/NullMax/FrontCam/fov_120/2022-01-12/2022-01-12-14-54/config/radar'
# pcd_file = '/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/pcd.txt'
# with open(pcd_file,'a+') as f:
#     for root,files in utils.walk(src):
#         for file_ in files:
#             file_ = os.path.basename(file_)
#             comment = file_ + '\n'
#             f.write(comment)

'''新frameid：老frameid'''
dict1 = {}
with open(relation_txtfile,'r') as f:
    for line in f.readlines():
        valuex = (((line.split("|")[0]).split("/")[-1]).split('.')[0]).split('_')[-1]
        keyx = ((line.split("|")[-1]).split('.')[0]).split('_')[-1]
        dict1[keyx] = valuex

'''pic列表'''
num_list = []
ori_num_list = []
for root,_,files in os.walk(src):
    for file_ in files:
        filenum = file_[10:-4]
        num_list.append(filenum)
for temp in num_list:
    ori_num = int(dict1[temp])
    ori_num_list.append(ori_num)

'''
pic列表对应的时间戳字典
字典格式key:vlaue
时间戳:老frameid
'''
int_time_list ={}
with open(timestamp_file,'r') as f:
    for timestamp_line in f.readlines():
        frameid = timestamp_line.split(' ')[-1]
        if int(frameid) in ori_num_list:
            int_time = int(timestamp_line.split(' ')[-4])
            int_time_list[int_time] = int(frameid)

'''老frameid：新frameid'''
dict2 = {}
with open(relation_txtfile,'r') as f:
    for line in f.readlines():
        keyx = (((line.split("|")[0]).split("/")[-1]).split('.')[0]).split('_')[-1]
        valuex= ((line.split("|")[-1]).split('.')[0]).split('_')[-1]
        dict2[keyx] = valuex

'''
获取pic列表对应的pcd文件，并修改成最新的frameid名称
'''
pcd_relation = '/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/pcd_relation.txt'
# with open(pcd_filetxt,'r') as f2,open(pcd_relation,'a+') as f3:
#     for pcd_file_line in f2.readlines():
#         pcd_file_line.strip()
#         pcd1 = int(pcd_file_line.split('.')[0])
#         pcd2 = int(pcd_file_line.split('.')[1])
#         pcdtime = int(pcd1*1000000 + pcd2/1000)
#         pcdtime2 = int((pcd1+1)*1000000 + pcd2/1000)
#         for temp in int_time_list.keys():
#             if pcdtime<int(temp)<pcdtime2:
#                 pcdname = pcd_file_line[:-1]
#                 ori_frameid = str(int_time_list[temp])
#                 rename_frameid = str(dict2[ori_frameid]) + '.pcd'
#                 comment=pcdname +'|' + ori_frameid + '|' +rename_frameid +'\n'
#                 f3.write(comment)

'''移动pcd文件'''
with open(pcd_relation,'r') as f4:
    for pcd_line in f4.readlines():
        pcd_line.strip()
        old_pcd = pcd_line.split('|')[0]
        new_pcd = pcd_line.split('|')[-1]
        os.system('cp {}/{} {}'.format(pcd_file,old_pcd,newpcd_filepath1))
        os.system('cp {}/{} {}/{}'.format(pcd_file,old_pcd,newpcd_filepath2,new_pcd))

                
            
            

