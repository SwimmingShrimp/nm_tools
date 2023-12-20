import os
pcd_path = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/merge/lable/pcd'
pic_path = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/merge/lable/FOV30'
new_path = '/data/NMtest/others/DataChoice/NullMax/3D/batch2/lable'

for root,_,files in os.walk(pcd_path):
    for file_ in files:
        idx = file_.split('.')[0].split('_')[-1]
        img_file = file_.replace('pcd','png')
        dst = os.path.join(new_path,idx)
        if not os.path.exists(dst): 
            os.makedirs(dst)
        command = 'cp {}/{} {}'.format(root,file_,dst)
        command2 = 'cp {}/{} {}'.format(pic_path,img_file,dst)
        print(command)
        print(command2)
        os.system(command)
        os.system(command2)