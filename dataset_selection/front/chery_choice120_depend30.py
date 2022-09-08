import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dst30',type=str,help='the path of fov30 img')
args = parser.parse_args()

dst30 = args.dst30

for root,_,files in os.walk(dst30):
    for file_ in files:
        if 'FOV30' in root:
            dst120 = root.replace('FOV30','FOV120')
            os.makedirs(dst120,exist_ok=True)
            date_hour = root.split('/')[-2]
            date_day = date_hour.rsplit('-',2)[0]
            src120_before = os.path.join('/data/Unlabeled/testset/NullMax/FrontCam/fov_120',date_day,date_hour,'video')
            src120_1 = os.path.join(src120_before,date_hour)
            src120_2 = os.path.join(src120_before,(date_hour+'_'))
            pathvalue = os.path.isdir(src120_1)
            if pathvalue:
                src120 = src120_1
            else:
                src120 = src120_2
            command = 'cp {}/{} {}'.format(src120,file_,dst120)
            print(command)
            os.system(command)
            
