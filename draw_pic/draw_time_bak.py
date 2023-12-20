import json
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_json_data(json_file):
    with open(json_file,'r') as f:
        try:
            json_data = json.load(f)
            return json_data
        except:
            print('json文件加载失败：{}'.format(json_file))
            return None
file_path = '/media/songbing/boot/0216/auto-driving_0215/bin/exp/6obs/log_20min/nm/sensor_camera.log'

interval_sampling = 3   #间隔多少帧采样
bar_width = 6           #柱状图的宽度

Detect_decoder = []
time_Detect_decoder = []
count_Detect_decoder = 0

Classify_decoder = []
time_Classify_decoder = []
count_Classify_decoder = 0

Entry_HwpCompute = []
time_Entry_HwpCompute = []
count_Entry_HwpCompute = 0

freespace = []
time_freespace = []
count_freespace = 0

lane_handle = []
time_lane_handle = []
count_lane_handle = 0
num_lane_handle = 0

lane_handle_send = []
time_lane_handle_send = []
count_lane_handle_send = 0

obstacle_postprocess = []
time_obstacle_postprocess = []
count_obstacle_postprocess = 0
num_obstacle_postprocess = 0

tracking = []
time_tracking = []
count_tracking = 0
num_tracking = 0

range = []
time_range = []
count_range = 0
num_range = 0

obstacle_fusion = []
time_obstacle_fusion = []
count_obstacle_fusion = 0

obstacle_send = []
time_obstacle_send = []
count_obstacle_send = 0

FilterObstacleFrame = []
time_FilterObstacleFrame = []
count_FilterObstacleFrame = 0

obstacle_num_list = []
obstacle_num = []
count_obstacle_num = 0

with open (file_path,'r') as f :
    for i,line in enumerate(f):
        line_data = line.strip().split()
        # print(line_data)
        '''Detect_decoder'''
        if 'detect_util.cpp:597]' in line_data:
            a_Detect_decoder = line_data[2]
        if 'detect_util.cpp:795]' in line_data:
            b_Detect_decoder = line_data[2]
            c_Detect_decoder = 1000000 * (60*(int(b_Detect_decoder.split('.')[0].split(':')[1]) - int(a_Detect_decoder.split('.')[0].split(':')[1]))+int(b_Detect_decoder.split('.')[0][-2:]) - int(a_Detect_decoder.split('.')[0][-2:]))+int(b_Detect_decoder.split('.')[-1]) - int(a_Detect_decoder.split('.')[-1])
            if c_Detect_decoder<0:
                print('c_Detect_decoder出现负值')
            time_Detect_decoder.append(c_Detect_decoder)
            Detect_decoder.append(count_Detect_decoder)
            count_Detect_decoder+=1

        '''Classify_decoder'''
        if 'detect_util.cpp:806]' in line_data:
            a_Classify_decoder = line_data[2]
        if 'detect_util.cpp:852]' in line_data:
            b_Classify_decoder = line_data[2]
            c_Classify_decoder = 1000000 * (60*(int(b_Classify_decoder.split('.')[0].split(':')[1]) - int(a_Classify_decoder.split('.')[0].split(':')[1]))+int(b_Classify_decoder.split('.')[0][-2:]) - int(a_Classify_decoder.split('.')[0][-2:]))+int(b_Classify_decoder.split('.')[-1]) - int(a_Classify_decoder.split('.')[-1])
            if c_Classify_decoder<0:
                print('c_Classify_decoder出现负值')
            time_Classify_decoder.append(c_Classify_decoder)
            Classify_decoder.append(count_Classify_decoder)
            count_Classify_decoder+=1

        '''Entry_HwpCompute'''
        if 'percept_computer.cpp:97]' in line_data:
            a_Entry_HwpCompute = line_data[2]
        if 'percept_computer.cpp:114]' in line_data:
            b_Entry_HwpCompute = line_data[2]
            c_Entry_HwpCompute = 1000000 * (60*(int(b_Entry_HwpCompute.split('.')[0].split(':')[1]) - int(a_Entry_HwpCompute.split('.')[0].split(':')[1]))+int(b_Entry_HwpCompute.split('.')[0][-2:]) - int(a_Entry_HwpCompute.split('.')[0][-2:]))+int(b_Entry_HwpCompute.split('.')[-1]) - int(a_Entry_HwpCompute.split('.')[-1])
            if c_Entry_HwpCompute < 0:
                print('c_Entry_HwpCompute出现负值')
                print(line_data[2])
            time_Entry_HwpCompute.append(c_Entry_HwpCompute)
            Entry_HwpCompute.append(count_Entry_HwpCompute)
            count_Entry_HwpCompute += 1

        '''freespace'''
        if 'free_space_handler.cpp:36]' in line_data:
            a_freespace = line_data[2]
        if 'free_space_handler.cpp:47]' in line_data:
            b_freespace = line_data[2]
            c_freespace = 1000000 * (60 * (int(b_freespace.split('.')[0].split(':')[1]) - int(
                a_freespace.split('.')[0].split(':')[1])) + int(b_freespace.split('.')[0][-2:]) - int(
                a_freespace.split('.')[0][-2:])) + int(b_freespace.split('.')[-1]) - int(
                a_freespace.split('.')[-1])
            if c_freespace < 0:
                print('c_freespace出现负值')
                print(line_data[2])
            time_freespace.append(c_freespace)
            freespace.append(count_freespace)
            count_freespace += 1

        '''lane_handle'''
        if 'lane_handler.cpp:202]' in line_data:
            a_lane_handle = line_data[2]
        if 'lane_handler.cpp:177]' in line_data:
            num_lane_handle +=1
            if num_lane_handle%2 == 0 :
                b_lane_handle = line_data[2]
                c_lane_handle = 1000000 * (60 * (int(b_lane_handle.split('.')[0].split(':')[1]) - int(
                    a_lane_handle.split('.')[0].split(':')[1])) + int(b_lane_handle.split('.')[0][-2:]) - int(
                    a_lane_handle.split('.')[0][-2:])) + int(b_lane_handle.split('.')[-1]) - int(
                    a_lane_handle.split('.')[-1])
                if c_lane_handle < 0:
                    print('c_lane_handle出现负值')
                    print(line_data[2])
                time_lane_handle.append(c_lane_handle)
                lane_handle.append(count_lane_handle)
                count_lane_handle += 1

        '''lane_handle_send'''
        if 'lane_handler.cpp:132]' in line_data:
            a_lane_handle_send = line_data[2]
        if 'lane_handler.cpp:149]' in line_data:
            b_lane_handle_send = line_data[2]
            c_lane_handle_send = 1000000 * (60 * (int(b_lane_handle_send.split('.')[0].split(':')[1]) - int(
                a_lane_handle_send.split('.')[0].split(':')[1])) + int(b_lane_handle_send.split('.')[0][-2:]) - int(
                a_lane_handle_send.split('.')[0][-2:])) + int(b_lane_handle_send.split('.')[-1]) - int(
                a_lane_handle_send.split('.')[-1])
            if c_lane_handle_send < 0:
                print('c_lane_handle_send出现负值')
                print(line_data[2])
            time_lane_handle_send.append(c_lane_handle_send)
            lane_handle_send.append(count_lane_handle_send)
            count_lane_handle_send += 1

        '''obstacle_postprocess'''
        if 'obstacle_perception.cpp:100]' in line_data:
            a_obstacle_postprocess = line_data[2]
        if 'obstacle_perception.cpp:103]' in line_data:
            num_obstacle_postprocess += 1
            if num_obstacle_postprocess % 2 == 0:
                b_obstacle_postprocess = line_data[2]
                c_obstacle_postprocess = 1000000 * (60 * (int(b_obstacle_postprocess.split('.')[0].split(':')[1]) - int(
                    a_obstacle_postprocess.split('.')[0].split(':')[1])) + int(b_obstacle_postprocess.split('.')[0][-2:]) - int(
                    a_obstacle_postprocess.split('.')[0][-2:])) + int(b_obstacle_postprocess.split('.')[-1]) - int(
                    a_obstacle_postprocess.split('.')[-1])
                if c_obstacle_postprocess < 0:
                    print('c_obstacle_postprocess出现负值')
                    print(line_data[2])
                time_obstacle_postprocess.append(c_obstacle_postprocess)
                obstacle_postprocess.append(count_obstacle_postprocess)
                count_obstacle_postprocess += 1

        '''tracking'''
        if 'obstacle_perception.cpp:110]' in line_data:
            a_tracking = line_data[2]
        if 'obstacle_perception.cpp:113]' in line_data:
            num_tracking += 1
            if num_tracking % 2 == 0:
                b_tracking = line_data[2]
                c_tracking = 1000000 * (60 * (int(b_tracking.split('.')[0].split(':')[1]) - int(
                    a_tracking.split('.')[0].split(':')[1])) + int(
                    b_tracking.split('.')[0][-2:]) - int(
                    a_tracking.split('.')[0][-2:])) + int(b_tracking.split('.')[-1]) - int(
                    a_tracking.split('.')[-1])
                if c_tracking < 0:
                    print('c_tracking出现负值')
                    print(line_data[2])
                time_tracking.append(c_tracking)
                tracking.append(count_tracking)
                count_tracking += 1

        '''range'''
        if 'obstacle_perception.cpp:137]' in line_data:
            a_range = line_data[2]
        if 'obstacle_perception.cpp:140]' in line_data:
            num_range += 1
            if num_range % 2 == 0:
                b_range = line_data[2]
                c_range = 1000000 * (60 * (int(b_range.split('.')[0].split(':')[1]) - int(
                    a_range.split('.')[0].split(':')[1])) + int(
                    b_range.split('.')[0][-2:]) - int(
                    a_range.split('.')[0][-2:])) + int(b_range.split('.')[-1]) - int(
                    a_range.split('.')[-1])
                if c_range < 0:
                    print('c_range出现负值')
                    print(line_data[2])
                time_range.append(c_range)
                range.append(count_range)
                count_range += 1

        '''obstacle_fusion'''
        if 'front_obstacle_perception.cpp:1074]' in line_data:
            a_obstacle_fusion = line_data[2]
        if 'front_obstacle_perception.cpp:1279]' in line_data:
            b_obstacle_fusion = line_data[2]
            c_obstacle_fusion = 1000000 * (60 * (int(b_obstacle_fusion.split('.')[0].split(':')[1]) - int(
                a_obstacle_fusion.split('.')[0].split(':')[1])) + int(
                b_obstacle_fusion.split('.')[0][-2:]) - int(
                a_obstacle_fusion.split('.')[0][-2:])) + int(b_obstacle_fusion.split('.')[-1]) - int(
                a_obstacle_fusion.split('.')[-1])
            if c_obstacle_fusion < 0:
                print('c_obstacle_fusion出现负值')
                print(line_data[2])
            time_obstacle_fusion.append(c_obstacle_fusion)
            obstacle_fusion.append(count_obstacle_fusion)
            count_obstacle_fusion += 1

        # '''obstacle_send'''
        # if 'obstacle_sender.cpp:356]' in line_data:
        #     a_obstacle_send = line_data[2]
        # if 'ipc_proxy.cpp:80]' and '/perception/obstacle_list' in line_data:
        #     b_obstacle_send = line_data[2]
        #     c_obstacle_send = 1000000 * (60 * (int(b_obstacle_send.split('.')[0].split(':')[1]) - int(
        #         a_obstacle_send.split('.')[0].split(':')[1])) + int(
        #         b_obstacle_send.split('.')[0][-2:]) - int(
        #         a_obstacle_send.split('.')[0][-2:])) + int(b_obstacle_send.split('.')[-1]) - int(
        #         a_obstacle_send.split('.')[-1])
        #     if c_obstacle_send < 0:
        #         print('c_obstacle_send出现负值')
        #         print(line_data[2])
        #     time_obstacle_send.append(c_obstacle_send)
        #     obstacle_send.append(count_obstacle_send)
        #     count_obstacle_send += 1

        # '''FilterObstacleFrame'''
        # if 'obstacle_track_filter.cpp:11]' in line_data:
        #     a_FilterObstacleFrame = line_data[2]
        # if 'obstacle_track_filter.cpp:121]' in line_data:
        #     b_FilterObstacleFrame = line_data[2]
        #     c_FilterObstacleFrame = 1000000 * (60 * (int(b_FilterObstacleFrame.split('.')[0].split(':')[1]) - int(
        #         a_FilterObstacleFrame.split('.')[0].split(':')[1])) + int(
        #         b_FilterObstacleFrame.split('.')[0][-2:]) - int(
        #         a_FilterObstacleFrame.split('.')[0][-2:])) + int(b_FilterObstacleFrame.split('.')[-1]) - int(
        #         a_FilterObstacleFrame.split('.')[-1])
        #     if c_FilterObstacleFrame < 0:
        #         print('c_FilterObstacleFrame出现负值')
        #         print(line_data[2])
        #     time_FilterObstacleFrame.append(c_FilterObstacleFrame)
        #     FilterObstacleFrame.append(count_FilterObstacleFrame)
        #     count_FilterObstacleFrame += 1

        '''obstacle_num'''
        if 'obstacle_handler.cpp:497]' in line_data:
            a_obstacle_num = int(line_data[-1])*100  #100 or 1000
            obstacle_num.append(a_obstacle_num)
            obstacle_num_list.append(count_obstacle_num)
            count_obstacle_num += 1

mean_obstacle_num = sum(obstacle_num)/len(obstacle_num_list)
min_obstacle_num = min(obstacle_num)
max_obstacle_num = max(obstacle_num)
print('统计的数量：%d'%len(obstacle_num_list))
print('平均obstacle_num：%f' % mean_obstacle_num)
print('最小obstacle_num：%f' % min_obstacle_num)
print('最大obstacle_num：%f' % max_obstacle_num)
print('******'*5)
obstacle_num_list = [obstacle_num for i,obstacle_num in enumerate(obstacle_num_list) if i%interval_sampling ==0 ]
obstacle_num = [num for i,num in enumerate(obstacle_num) if i%interval_sampling ==0 ]

# mean_FilterObstacleFrame = sum(time_FilterObstacleFrame)/len(FilterObstacleFrame)
# min_FilterObstacleFrame = min(time_FilterObstacleFrame)
# max_FilterObstacleFrame = max(time_FilterObstacleFrame)
# print('统计的数量：%d'%len(FilterObstacleFrame))
# print('平均FilterObstacleFrame：%f' % mean_FilterObstacleFrame)
# print('最小FilterObstacleFrame：%f' % min_FilterObstacleFrame)
# print('最大FilterObstacleFrame：%f' % max_FilterObstacleFrame)
# print('******'*5)
# FilterObstacleFrame = [FilterObstacleFrame1 for i,FilterObstacleFrame1 in enumerate(FilterObstacleFrame) if i%interval_sampling ==0 ]
# time_FilterObstacleFrame = [time_FilterObstacleFrame1 for i,time_FilterObstacleFrame1 in enumerate(time_FilterObstacleFrame) if i%interval_sampling ==0 ]

# mean_obstacle_send = sum(time_obstacle_send)/len(obstacle_send)
# min_obstacle_send = min(time_obstacle_send)
# max_obstacle_send = max(time_obstacle_send)
# print('统计的数量：%d'%len(obstacle_send))
# print('平均obstacle_send：%f' % mean_obstacle_send)
# print('最小obstacle_send：%f' % min_obstacle_send)
# print('最大obstacle_send：%f' % max_obstacle_send)
# print('******'*5)
# obstacle_send = [obstacle_send1 for i,obstacle_send1 in enumerate(obstacle_send) if i%interval_sampling ==0 ]
# time_obstacle_send = [time_obstacle_send1 for i,time_obstacle_send1 in enumerate(time_obstacle_send) if i%interval_sampling ==0 ]


mean_obstacle_fusion = sum(time_obstacle_fusion)/len(obstacle_fusion)
min_obstacle_fusion = min(time_obstacle_fusion)
max_obstacle_fusion = max(time_obstacle_fusion)
print('统计的数量：%d'%len(obstacle_fusion))
print('平均obstacle_fusion：%f' % mean_obstacle_fusion)
print('最小obstacle_fusion：%f' % min_obstacle_fusion)
print('最大obstacle_fusion：%f' % max_obstacle_fusion)
print('******'*5)
obstacle_fusion = [obstacle_fusion1 for i,obstacle_fusion1 in enumerate(obstacle_fusion) if i%interval_sampling ==0 ]
time_obstacle_fusion = [time_obstacle_fusion1 for i,time_obstacle_fusion1 in enumerate(time_obstacle_fusion) if i%interval_sampling ==0 ]

mean_range = sum(time_range)/len(range)
min_range = min(time_range)
max_range = max(time_range)
print('统计的数量：%d'%len(range))
print('平均range：%f' % mean_range)
print('最小range：%f' % min_range)
print('最大range：%f' % max_range)
print('******'*5)
range = [range1 for i,range1 in enumerate(range) if i%interval_sampling ==0 ]
time_range = [time_range1 for i,time_range1 in enumerate(time_range) if i%interval_sampling ==0 ]

mean_tracking = sum(time_tracking)/len(tracking)
min_tracking = min(time_tracking)
max_tracking = max(time_tracking)
print('统计的数量：%d'%len(tracking))
print('平均tracking：%f' % mean_tracking)
print('最小tracking：%f' % min_tracking)
print('最大tracking：%f' % max_tracking)
print('******'*5)
tracking = [tracking1 for i,tracking1 in enumerate(tracking) if i%interval_sampling ==0 ]
time_tracking = [time_tracking1 for i,time_tracking1 in enumerate(time_tracking) if i%interval_sampling ==0 ]

mean_obstacle_postprocess = sum(time_obstacle_postprocess)/len(obstacle_postprocess)
min_obstacle_postprocess = min(time_obstacle_postprocess)
max_obstacle_postprocess = max(time_obstacle_postprocess)
print('统计的数量：%d'%len(obstacle_postprocess))
print('平均obstacle_postprocess：%f' % mean_obstacle_postprocess)
print('最小obstacle_postprocess：%f' % min_obstacle_postprocess)
print('最大obstacle_postprocess：%f' % max_obstacle_postprocess)
print('******'*5)
obstacle_postprocess = [obstacle_postprocess1 for i,obstacle_postprocess1 in enumerate(obstacle_postprocess) if i%interval_sampling ==0 ]
time_obstacle_postprocess = [time_obstacle_postprocess1 for i,time_obstacle_postprocess1 in enumerate(time_obstacle_postprocess) if i%interval_sampling ==0 ]

mean_lane_handle_send = sum(time_lane_handle_send)/len(lane_handle_send)
min_lane_handle_send = min(time_lane_handle_send)
max_lane_handle_send = max(time_lane_handle_send)
print('统计的数量：%d'%len(lane_handle_send))
print('平均lane_handle_send：%f' % mean_lane_handle_send)
print('最小lane_handle_send：%f' % min_lane_handle_send)
print('最大lane_handle_send：%f' % max_lane_handle_send)
print('******'*5)
lane_handle_send = [lane_handle_send1 for i,lane_handle_send1 in enumerate(lane_handle_send) if i%interval_sampling ==0 ]
time_lane_handle_send = [time_lane_handle_send1 for i,time_lane_handle_send1 in enumerate(time_lane_handle_send) if i%interval_sampling ==0 ]

mean_lane_handle = sum(time_lane_handle)/len(lane_handle)
min_lane_handle = min(time_lane_handle)
max_lane_handle = max(time_lane_handle)
print('统计的数量：%d'%len(lane_handle))
print('平均lane_handle：%f' % mean_lane_handle)
print('最小lane_handle：%f' % min_lane_handle)
print('最大lane_handle：%f' % max_lane_handle)
print('******'*5)
lane_handle = [lane_handle1 for i,lane_handle1 in enumerate(lane_handle) if i%interval_sampling ==0 ]
time_lane_handle = [time_lane_handle1 for i,time_lane_handle1 in enumerate(time_lane_handle) if i%interval_sampling ==0 ]

mean_freespace = sum(time_freespace)/len(freespace)
min_freespace = min(time_freespace)
max_freespace = max(time_freespace)
print('统计的数量：%d'%len(freespace))
print('平均freespace：%f' % mean_freespace)
print('最小freespace：%f' % min_freespace)
print('最大freespace：%f' % max_freespace)
print('******'*5)
freespace = [freespace1 for i,freespace1 in enumerate(freespace) if i%interval_sampling ==0 ]
time_freespace = [time_freespace1 for i,time_freespace1 in enumerate(time_freespace) if i%interval_sampling ==0 ]

mean_Entry_HwpCompute = sum(time_Entry_HwpCompute)/len(Entry_HwpCompute)
min_Entry_HwpCompute = min(time_Entry_HwpCompute)
max_Entry_HwpCompute = max(time_Entry_HwpCompute)
print('统计的数量：%d'%len(Entry_HwpCompute))
print('平均Entry_HwpCompute：%f' % mean_Entry_HwpCompute)
print('最小Entry_HwpCompute：%f' % min_Entry_HwpCompute)
print('最大Entry_HwpCompute：%f' % max_Entry_HwpCompute)
print('******'*5)
Entry_HwpCompute = [Entry_HwpCompute1 for i,Entry_HwpCompute1 in enumerate(Entry_HwpCompute) if i%interval_sampling ==0 ]
time_Entry_HwpCompute = [time_Entry_HwpCompute1 for i,time_Entry_HwpCompute1 in enumerate(time_Entry_HwpCompute) if i%interval_sampling ==0 ]

mean_Classify_decoder = sum(time_Classify_decoder)/len(Classify_decoder)
min_Classify_decoder = min(time_Classify_decoder)
max_Classify_decoder = max(time_Classify_decoder)
print('统计的数量：%d'%len(Classify_decoder))
print('平均Classify_decoder：%f' % mean_Classify_decoder)
print('最小Classify_decoder：%f' % min_Classify_decoder)
print('最大Classify_decoder：%f' % max_Classify_decoder)
print('******'*5)
Classify_decoder = [Classify_decoder1 for i,Classify_decoder1 in enumerate(Classify_decoder) if i%interval_sampling ==0 ]
time_Classify_decoder = [time_Classify_decoder1 for i,time_Classify_decoder1 in enumerate(time_Classify_decoder) if i%interval_sampling ==0 ]

mean_Detect_decoder = sum(time_Detect_decoder)/len(Detect_decoder)
min_Detect_decoder = min(time_Detect_decoder)
max_Detect_decoder = max(time_Detect_decoder)
print('统计的数量：%d'%len(Detect_decoder))
print('平均Detect_decoder：%f' % mean_Detect_decoder)
print('最小Detect_decoder：%f' % min_Detect_decoder)
print('最大Detect_decoder：%f' % max_Detect_decoder)
print('******'*5)
Detect_decoder = [Detect_decoder1 for i,Detect_decoder1 in enumerate(Detect_decoder) if i%interval_sampling ==0 ]
time_Detect_decoder = [time_Detect_decoder1 for i,time_Detect_decoder1 in enumerate(time_Detect_decoder) if i%interval_sampling ==0 ]


'''第一组'''
'''折线图'''
# plt.plot(Detect_decoder,time_Detect_decoder,c='b')
# plt.plot(Classify_decoder,time_Classify_decoder,c='g')
# plt.plot(obstacle_postprocess,time_obstacle_postprocess,c ='b',marker='*')
# plt.plot(tracking,time_tracking,c ='g',marker='*')
# plt.plot(range,time_range,c ='r',marker='*')
# plt.plot(obstacle_fusion,time_obstacle_fusion,c ='r',marker='o')
# plt.bar(obstacle_num_list,obstacle_num, color='orange')
'''堆叠柱状图'''
# plt.bar(Classify_decoder, np.array(time_Detect_decoder), width=bar_width, label='time_Detect_decoder', color='b')
# plt.bar(Classify_decoder, np.array(time_Classify_decoder), width=bar_width, label='time_Classify_decoder', color='g', bottom=np.array(time_Detect_decoder))
# plt.bar(Classify_decoder, np.array(time_obstacle_postprocess), width=bar_width, label='time_obstacle_postprocess', color='r',bottom=np.array(time_Detect_decoder) + np.array(time_Classify_decoder) )
# plt.bar(Classify_decoder, np.array(time_tracking), width=bar_width, label='time_tracking', color='silver',bottom=np.array(time_Detect_decoder) + np.array(time_Classify_decoder) +np.array(time_obstacle_postprocess) )
# plt.bar(Classify_decoder, np.array(time_range), width=bar_width, label='time_range', color='#CD853F',bottom=np.array(time_Detect_decoder) + np.array(time_Classify_decoder) +np.array(time_obstacle_postprocess) + np.array(time_tracking))
# plt.bar(Classify_decoder, np.array(time_obstacle_fusion), width=bar_width, label='time_obstacle_fusion', color='aquamarine',bottom=np.array(time_Detect_decoder) + np.array(time_Classify_decoder) +np.array(time_obstacle_postprocess) + np.array(time_tracking)+np.array(time_range))
# plt.plot(obstacle_num_list,obstacle_num, color='orange')

'''第二组'''
'''折线图'''
# plt.plot(Entry_HwpCompute,time_Entry_HwpCompute,c='r')  #总的单独
# plt.bar(obstacle_num_list,obstacle_num, color='orange')
'''堆叠柱状图'''
# plt.bar(Entry_HwpCompute, time_Entry_HwpCompute, width=bar_width, label='time_Entry_HwpCompute', color='g')
# plt.plot(obstacle_num_list,obstacle_num, color='r')


'''第三组'''
'''折线图'''
# plt.plot(freespace,time_freespace,c='y')
# plt.plot(lane_handle,time_lane_handle,marker='.')
# plt.plot(lane_handle_send,time_lane_handle_send,marker='*')
'''堆叠柱状图'''
plt.bar(freespace, np.array(time_freespace), width=bar_width, label='time_freespace', color='gold')
plt.bar(lane_handle, np.array(time_lane_handle), width=bar_width, label='time_lane_handle', color='silver', bottom=np.array(time_freespace))
plt.bar(lane_handle_send, np.array(time_lane_handle_send), width=bar_width, label='time_lane_handle_send', color='#CD853F', bottom=np.array(time_freespace)+np.array(time_lane_handle))
plt.plot(obstacle_num_list,obstacle_num, color='orange')


# plt.legend(['time_Detect_decoder','time_Classify_decoder','time_obstacle_postprocess','time_tracking','time_range','time_obstacle_fusion','time_obstacle_send','obstacle_num'], loc='best')              #'''第一组'''
plt.legend( loc='best')                                                                                                                                      #'''第二组'''
# plt.legend(['time_freespace','time_lane_handle','time_lane_handle_send','obstacle_num'], loc='best')                                                                                                      #'''第三组'''
plt.xlabel('n')
plt.ylabel('time')
plt.xlim(0,1500)
plt.ylim(0,50000)   #40000 or 150000 or
plt.savefig(file_path.split('.')[0]+'.png')
plt.show()
plt.close()





