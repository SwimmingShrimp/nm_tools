import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('benchmarkid',type=str)
args = parser.parse_args()
benchmarkid = args.benchmarkid

relation_txt = '/data1/NMtest/others/DataChoice/NullMax/2D/2D_batch1_ori_1/relation.txt'
dst = '/data1/NMtest/CornerCaseAndPseudoGT/JIRA/chery_front_120_30_jira/FAULT-1547/case6/input'
with open(relation_txt,'r') as f:
    for line in f.readlines():
        real_date2 = (line.split('|')[0]).split('/')[8]
        real_date1 = real_date2.rsplit('-',2)[0]
        new_frame_id = ((line.split('|')[-1]).split(".")[0]).split('_')[-1]
        old_frame_id = (((line.split('|')[0]).split('/')[-1]).split(".")[0]).split('_')[-1]
        src_120 = os.path.join('/data1/Unlabeled/testset/NullMax/FrontCam/fov_120',real_date1,real_date2,'oimg')
        src_30= src_120.replace('fov_120','fov_30')
        if int(new_frame_id) == int(benchmarkid) and 'vc1' not in line and 'fov_120' and 'day' in line:
            print(line)
            for i in range(20):
                filename_num = int(old_frame_id) +5 -i
                filename = 'frame_vc2_' + str(filename_num) + '.png'
                newfilename = filename.replace('vc2','vc1')
                dst120 = os.path.join(dst,'FOV120')
                os.makedirs(dst120, exist_ok=True)
                command1 = 'cp {}/{} {}/{}'.format(src_120 ,filename ,dst120,newfilename)
                i +=1
                os.system(command1)
                # print(command1)
        elif int(new_frame_id) == int(benchmarkid) and 'fov_30' and 'day' in line:
            print(line)
            for j in range(20):
                filename_num2 = int(old_frame_id) +5 -j
                filename2 = 'frame_vc1_' + str(filename_num2) + '.png'
                newfilename2 = filename2.replace('vc1','vc2')
                dst30 = os.path.join(dst,'FOV30')
                os.makedirs(dst30, exist_ok=True)
                command2 = 'cp {}/{} {}/{}'.format(src_30 ,filename2 ,dst30,newfilename2)
                j +=1
                # print(command2)
                os.system(command2)

            
            
        

