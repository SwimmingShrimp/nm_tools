import os
pcd_path = '/data1/NMtest/others/DataChoice/NullMax/3D/pcd_2022-01-12-14-54/rename'
pic_path = '/data1/NMtest/others/DataChoice/NullMax/3D/lable_2022-01-12-14-54/FOV30'
new_path = '/data1/NMtest/others/DataChoice/NullMax/3D/lable'

for root,_,files in os.walk(pcd_path):
    for file_ in files:
        idx = file_[:-4]
        dir_file = 'frame_vc2_' + idx +'.png'
        dst = os.path.join(new_path,idx)
        if not os.path.exists(dst): 
            os.makedirs(dst)
        command = 'cp {}/{} {}'.format(root,file_,dst)
        command2 = 'cp {}/{} {}'.format(pic_path,dir_file,dst)
        print(command)
        print(command2)
        os.system(command)
        os.system(command2)