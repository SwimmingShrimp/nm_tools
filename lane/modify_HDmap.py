from distutils import command
from operator import ne
import sys
sys.path.append("..")
import utils
import os


txtfile = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/ori_data/relation.txt'
dict1 = {}
with open(txtfile,'r') as f:
    for line in f.readlines():
        keyx = ((line.split("|")[0]).split("/")[-1]).split('.')[0]
        valuex = ((line.split("|")[-1]).split('.')[0]).split('_')[-1]
        dict1[keyx] = valuex

'''
修改时间戳数据
'''
def modify_timestamp():
    timestampfile = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/ori_data/timestamp.log'
    new_timestampfile = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/rename_data/timestamp.log'
    with open(timestampfile,'r') as f2:
        with open(new_timestampfile,'a+') as f3:
            for line in f2.readlines():
                line = line.strip()            
                frame_id = line.split(' ')[-1]            
                if frame_id in dict1.keys():
                    comment = line.rsplit(' ',1)[0] + ' ' + dict1[frame_id] + '\n'
                    f3.write(comment)
    num =0
    with open(new_timestampfile,'r') as f:
        for line in f.readlines():
            num +=1
    print(num)
'''
修改车身数据
'''
def modify_vehicle():
    vehicle = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/ori_data/vehicle.log'
    new_vehicle = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/rename_data/vehicle.log'
    with open(vehicle,'r') as f4:
        with open(new_vehicle,'a+') as f5:
            for line in f4.readlines():
                line = line.strip()            
                frame_id = line.split(' ')[-1]            
                if frame_id in dict1.keys():
                    comment = line.rsplit(' ',1)[0] + ' ' + dict1[frame_id] + '\n'
                    f5.write(comment)
    num =0
    with open(new_vehicle,'r') as f:
        for line in f.readlines():
            num +=1
    print(num)
'''
修改novatel的数据
'''        
def modify_novatel():
    novatel = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/ori_data/novatel.txt'
    new_novatel = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/HDmap/rename_data/novatel.txt'
    with open(novatel,'r') as f6:
        with open(new_novatel,'a+') as f7:
            for line in f6.readlines():
                line = line.strip()            
                frame_id = line.split(' ')[0]
                if frame_id in dict1.keys():
                    comment =  dict1[frame_id] + ' ' +  line.split(' ',1)[-1] +  '\n'
                    f7.write(comment)
    num =0
    with open(new_novatel,'r') as f:
        for line in f.readlines():
            num +=1
    print(num)

def main():
    modify_timestamp()
    modify_vehicle()
    modify_novatel()


if __name__=="__main__":
    main()