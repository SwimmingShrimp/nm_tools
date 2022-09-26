import sys
sys.path.append('..')
import utils
import os
import matplotlib.pyplot as plt
import cv2

# # img = cv2.imread('/data/NMtest/others/PlayBackPic/2022-01-12-14-54/1/FOV30/frame_vc1_8448.png')
# # print(img,type(img))

# idx = 0 
# src = '/home/lixialin/Videos/mona/side_right_front'
# for root, _,files in os.walk(src):
#     files = sorted(files, key=lambda x:int(x.split('.')[0]))
#     for file_ in files:
#         newfile = str(idx) + '.png'
#         os.system('mv {}/{} {}/{}'.format(root,file_,root,newfile))
#         idx +=1
        # num = os.path.basename(file_).split('_')[-1].split('.')[0]
        # num = os.path.basename(file_).split('.')[0]
        # print(num)
        # if int(num)<10:
        #     newfile= 'frame_vc1_0' + str(int(num)) + '.yuv'
        #     os.system('mv {} {}/{}'.format(file_,root,newfile))
        # # else:
        #     newfile= 'frame_vc1_' + str(int(num)) + '.png'
        #     os.system('mv {} {}/{}'.format(file_,root,newfile))
        

# src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/0_temp/2022-01-12-14-54/2/FOV120'
# for root,_ ,files in os.walk(src):
#     for file_ in files:
#         newfile = file_.replace('vc2','vc1')
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


def draw_recall():
    x = [1,2,3,4,5,6,7,8]
    y1_cust_request_recall = [14.9968,13.99,14.9866,13.9878,13.9877,14.487,13.9882,13.9952]
    # y2_perce_day_recall = [98.8,97.5,96.8,92.6,97.7,97.6,98.8]
    # y3_perce_night_recall = [98.5,88,98.1,89,93.8,96.4,100]

    plt.title('online realtime frame rate')
    plt.plot(x, y1_cust_request_recall, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
    # plt.plot(x, y2_perce_day_recall, marker='o', markersize=3)
    # plt.plot(x, y3_perce_night_recall, marker='o', markersize=3)

    for a, b in zip(x, y1_cust_request_recall):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
    # for a, b in zip(x, y2_perce_day_recall):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    # for a, b in zip(x, y3_perce_night_recall):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    # plt.legend(['cust_request_recall', 'perce_day_recall', 'perce_night_recall'])  # 设置折线名称
    plt.show()  # 显示折线图

draw_recall()