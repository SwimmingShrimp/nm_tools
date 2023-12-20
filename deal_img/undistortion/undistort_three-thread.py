# coding:UTF-8
# Author:WangLiang
# DATA:20230813上午9:40
# Instruction：去畸变脚本
import math
import os, sys, cv2
import re
import threading
import time
from argparse import ArgumentParser

import numpy as np
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import kafka_errors
import traceback
import json


def mkdir(p):
    if not os.path.exists(p):
        os.makedirs(p)



def get_video_lst(clip_dir):
    thread_num = 3
    video_lst = []
    for root, dir, files in os.walk(clip_dir):
        for f in files:
            if f.endswith('.mp4'):
                video_path = os.path.join(root, f)
                video_lst.append(video_path)
    video_lst = list(set(video_lst))
    step = len(video_lst) // thread_num
    video_lst = [video_lst[:1 * step], \
                 video_lst[1 * step:2 * step], \
                 video_lst[2 * step:]]
    return video_lst


# five_min_path:/mount_point/raw_data/mondeo4/20230824/camera
def get_sort_txt(five_min_path):
    print(five_min_path)
    file_dict = {"front_far.txt": 1, "front_near.txt": 2, "side_left_front.txt": 3, "side_left_rear.txt": 4,\
                 "side_right_front.txt": 5, "side_right_rear.txt": 6, \
                 "fish_back.txt": 7, "fish_front.txt": 8, "fish_left.txt": 9, "fish_right.txt": 10,\
                 "back_middle.txt": 11, "back_middle_2M.txt": 12, \
                 }
    sort_dict = {1: "front_far.txt", 2: "front_near.txt", 3: "side_left_front.txt", 4: "side_left_rear.txt",\
                 5: "side_right_front.txt", 6: "side_right_rear.txt", \
                 7: "fish_back.txt", 8: "fish_front.txt", 9: "fish_left.txt", 10: "fish_right.txt",\
                 11: "back_middle.txt", 12: "back_middle_2M.txt"}
    file_num_lst = []
    for root, dirs, files in os.walk(five_min_path):
        for file in files:
            if file in file_dict.keys():
                file_num_lst.append(file_dict[file]) # file_num_lst = [1,2,3,4....]
    file_num_lst.sort()
    return os.path.join(five_min_path,sort_dict[file_num_lst[0]])


def get_img_dic(video_path, img_type):
    img_name_dic = {}
    video_txt = get_sort_txt(video_path)
    print(video_txt)
    if not os.path.exists(video_txt):
        return False
    with open(video_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            num = line.strip().split(' ')[1]
            time_stamp = line.strip().split(' ')[-1]
            # num = line.strip().split(' ')[0].split(':')[1]
            # time_stamp = line.strip().split(' ')[1].split(':')[1]
            img_name_dic[int(num)] = time_stamp + '.' + img_type
    return img_name_dic

# /mount_point/raw_data/mondeo4/20230824/140650/ 
def get_param_path(clip_dir):
    file_dic = {}
    if clip_dir.endswith('/'):
        clip_dir = clip_dir.rsplit('/',1)[0]
    deal_time = int(clip_dir.split('/')[-2])
    time_difference = 999999999
    json_file = ''
    for f in os.listdir(f'{clip_dir}/../../calibration/'):
        print(f)
        if 'calibration'in f and f.endswith('.json'):
            json_time = int(f.split('.')[0].split('_')[1][:8])
            if deal_time > json_time:
                if time_difference > (deal_time - json_time):
                    time_difference = deal_time - json_time
                    json_file = os.path.join(f'{clip_dir}/../../calibration/',f)
                else:
                    continue
            else:
                continue
    print(json_file)
    return json_file



# 获取相机内外参和畸变系数
def get_cameraMatrix_distCoeffs(clip_dir, undistort_type):
    param_path = get_param_path(clip_dir)
    print(11111111111111)
    print(param_path)
    if len(param_path) <=0:
        print("相机参数文件获取失败，请检查相机参数文件！！！")
        sys.exit()
    camera_position = ["back_middle","back_middle_2M","fish_back","fish_front","fish_left","fish_right","front_far",\
                       "front_near","side_left_front","side_left_rear","side_right_front","side_right_rear"]
    param_dic = {} # index0是相机内外参 index1是去畸变系数
    if os.path.exists(param_path):
        with open(param_path, 'r') as f:
            json_data = json.load(f)
            for position in camera_position:
                if position in json_data.keys():
                    try:
                        fx = json_data[position]['intrinsics']['fx']
                        fy = json_data[position]['intrinsics']['fy']
                        cx = json_data[position]['intrinsics']['cx']
                        cy = json_data[position]['intrinsics']['cy']
                        k1 = json_data[position]['distortions']['k1']
                        k2 = json_data[position]['distortions']['k2']
                        p1 = json_data[position]['distortions']['p1']
                        p2 = json_data[position]['distortions']['p2']
                        k3 = json_data[position]['distortions']['k3']
                        k4 = json_data[position]['distortions']['k4']
                        k5 = json_data[position]['distortions']['k5']
                        k6 = json_data[position]['distortions']['k6']
                        width = json_data[position]['width']
                        height = json_data[position]['width']
                        camera_fov = json_data[position]['camera_fov']
                    except KeyError:
                        sys.stdout.write(f'参数文件错误')
                        sys.exit(1)  # failed
                    if undistort_type == 'img_fullfov_undistort':
                        fx = width/2/math.tan(camera_fov/2/180*math.pi)
                        fy = width/2/math.tan(camera_fov/2/180*math.pi)
                    cameraMatrix = np.array([[fx, 0, cx],
                                  [0, fy, cy],
                                  [0, 0, 1]])
                    distCoeffs = np.array([k1, k2, p1, p2])
                    if k3 != 0 or k4 != 0 or k5 != 0 or k6 != 0:
                        distCoeffs = np.array([k1, k2, p1, p2, k3, k4, k5, k6])
                    param_dic[position]=[cameraMatrix,distCoeffs]
                else:
                    sys.stdout.write(f'参数文件视角信息不存在！\n')

    else:
        # 如果文件不存在，就使用默认值
        cameraMatrix = None
        distCoeffs = None
        cameraMatrix_new = None
        sys.stdout.write(f'不存在标定参数文件')
        sys.exit(1)  # failed

    return param_dic



# /prepared/parsed_data
# /mount_point/raw_data

def parse_img_normal_undistort(producer, topic, video_path_lst, img_type, interval, start_time, undistort_type, param_dic):
    for video_path in video_path_lst:
        if video_path.endswith('.mp4'):
            video_dir = os.path.dirname(video_path)
            img_name_dic = get_img_dic(video_dir, img_type)
            save_dir = video_dir.replace('/mount_point/raw_data', '/prepared/parsed_data')
            fov = video_path.split('/')[-1].split('.')[0]
            cnt = 0
            cap = cv2.VideoCapture(video_path)
            while cap.isOpened():
                ret, frame = cap.read()  # ret表示读取成功，frame是从视频中读取到的帧，即图片
                if ret:
                    cameraMatrix = param_dic[fov][0]
                    distCoeffs = param_dic[fov][1]

                    dst_dir = os.path.join(save_dir, undistort_type, fov)
                    mkdir(dst_dir)
                    img_name = img_name_dic.get(cnt, 'error.jpg')
                    dst_img = os.path.join(dst_dir, img_name)
                    if (cnt) % interval == 0:
                        img_distort = cv2.undistort(frame, cameraMatrix, distCoeffs, None, cameraMatrix)
                        cv2.imwrite(dst_img, img_distort)
                        print(dst_img)
                    cnt += 1
                else:
                    break

    # 处理完一个五分钟，同步处理进度
    mutex.acquire()
    process_cnt += 1
    mutex.release()
    end_time = time.time()
    take_time = end_time - start_time
    update_type = 1
    clip_dir = video_dir.rsplit('/', 1)[0]
    update_dir = clip_dir
    parsed_dir =  update_dir.replace('/mount_point/raw_data', '/prepared/parsed_data')
    state = 2
    send_kafka_msg(producer, topic, 12, update_type, update_dir, parsed_dir, undistort_type, state, take_time)


# 同步发送kafka 消息
def send_kafka_msg(producer, topic, process, update_type, update_dir, parsed_dir, undistort_type=True, state=0, take_time=0):
    return
    if update_type == 1:
        total_cnt = 12
    # 按天抽帧开始发送消息
    if undistort_type == 'img_fullfov_undistort':
        img_normal_undistort = False
        img_fullfov_undistort = True
    else:
        img_normal_undistort = True
        img_fullfov_undistort = False
    process_dict = {
        "update_type": update_type,  # 更新数据粒度, 枚举值【day:更新天的状态，clip：更新5分钟的状态】
        "dir": update_dir,  # day/clip的绝对路径
        "parsed_dir": parsed_dir,
        "process": f'{process}/{total_cnt}',  # day/clip的处理进度
        "failed": 0,  # 处理失败数
        "failed_reason": "",
        "img_normal_undistort":img_normal_undistort,
        "img_fullfov_undistort": img_fullfov_undistort,
        "state": state,  # day/clip处理状态
        "take_time": take_time  # day/clip处理耗时
    }
    msg = json.dumps(process_dict, ensure_ascii=True).encode("utf-8")
    print("---send msg---\n", msg)
    future = producer.send(topic, value=msg)  # 此处传入kafka的topic
    try:
        res = future.get(timeout=5)  # 监控一定时间内是否发送成功
        print('send success get res', res)
    except Exception as e:  # 发送失败抛出kafka_errors
        print(e)


# python3.8 videoshot_all.py
def main():
    start_time = time.time()
    parser = ArgumentParser()
    parser.add_argument('clip_dir', help='path of day directory')
    parser.add_argument('--img_type', default='jpg', help='img type:png jpg bmp...')
    parser.add_argument('--undistort_type', default='img_normal_undistort', help='undistort_type:img_normal_undistort,img_fullfov_undistort')
    parser.add_argument('--interval', default=1, help='Process type：parse_video,parse_pcd...', type=int)
    parser.add_argument('--kafka_server', default='10.10.9.235:30003',
                        help='kafka ip+port 如:10.10.9.235:30003 【测试环境】10.10.9.235:30403 【生产环境】')
    parser.add_argument('--topic', default='test', help='kafa topic')

    args = parser.parse_args()

    clip_dir = args.clip_dir  # clip路径
    img_type = args.img_type  # 图片类型 jpg/png
    undistort_type = args.undistort_type #
    kafka_server = args.kafka_server  # kafka ip+port 如:10.10.9.235:30003 【测试环境】10.10.9.235:30403 【生产环境】
    topic = args.topic  # topic 名称 videoshot
    interval = args.interval  # 抽帧间隔  默认为1

    print(f'start parse video and normal undistort...')
    print(f'video dir:{clip_dir}\nimg type:{img_type}\ninterval:{interval}')

    video_lst = get_video_lst(clip_dir)

    # 开始解析,发送kafka消息
    update_type = 1
    update_dir = clip_dir
    parsed_dir = update_dir.replace('/mount_point/raw_data', '/prepared/parsed_data')
    state = 1
    process = 0
    take_time = 0

    # producer = KafkaProducer(bootstrap_servers=[kafka_server])  # 此处传入kafka的地址和端口
    producer = ''
    send_kafka_msg(producer, topic, process, update_type, update_dir, parsed_dir, undistort_type, state, take_time)

    # 获取畸变系数 {“front_far”:[cameraMatrix,distCoeffs],"front_near":[cameraMatrix,distCoeffs]}
    param_dic = get_cameraMatrix_distCoeffs(clip_dir, undistort_type)

    # 解析图片
    thread_list = []
    for index, video_path_lst in enumerate(video_lst):
        t_num = 't' + str(index)
        t_num = threading.Thread(target=parse_img_normal_undistort,
                                 args=(producer, topic, video_path_lst, img_type, interval, start_time, undistort_type, param_dic))
        thread_list.append(t_num)

    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    # 解析结束,发送kafka消息
    process = 6000
    end_time = time.time()
    take_time = end_time - start_time
    state = 2
    send_kafka_msg(producer, topic, process, update_type, update_dir, parsed_dir, undistort_type, state, take_time)

    print(f'{clip_dir} completed video parsing!!!')
    # producer.close()


if __name__ == "__main__":
    main()
