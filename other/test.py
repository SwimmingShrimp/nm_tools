import sys
sys.path.append('..')
import utils
import os
import cv2

img = cv2.imread('/data/NMtest/others/PlayBackPic/2022-01-12-14-54/1/FOV30/frame_vc1_8448.png')
print(img,type(img))

# src = '/media/lixialin/lxl/result/lane/lane30'
# for root, files in utils.walk(src):
#     for file_ in files:
#         num = os.path.basename(file_).split('_')[-1].split('.')[0]
#         # num = os.path.basename(file_).split('.')[0]
#         print(num)
#         if int(num)<10:
#             newfile= 'frame_vc1_0' + str(int(num)) + '.png'
#             os.system('mv {} {}/{}'.format(file_,root,newfile))
#         else:
#             newfile= 'frame_vc1_' + str(int(num)) + '.png'
#             os.system('mv {} {}/{}'.format(file_,root,newfile))
        

# src = '/home/lixialin/Pictures/2/FOV30'
# for root,_ ,files in os.walk(src):
#     for file_ in files:
#         newfile = file_.replace('vc1','vc2')
#         os.system('mv {}/{} {}/{}'.format(root,file_,root,newfile))

# json_data = utils.get_json_data('/home/lixialin/Downloads/json/night/night.json')
# dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/1_json/chery/2d_lable_merge/night_rename/night.json'
# new_json = []
# for temp in json_data:
#     new_temp = temp
#     with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/0_dataset/Qirui/2D/new_night/relation_night.txt','r') as f:
#         for line in f.readlines():
#             oldname = line.split('|')[0].split('/')[-1]
#             num = int(oldname.split('.')[0].split('_')[-1])
#             if num <290:
#                 continue
#             newname = line.split('|')[-1][:-1]
#             if temp["filename"] == oldname:
#                 temp["filename"] = newname
#                 new_json.append(temp)
# utils.write_json_data(dst,new_json)