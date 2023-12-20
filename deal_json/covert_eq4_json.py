from cantools import database
import json
import pandas as pd
import numpy as np
import struct
import collections
import os
import copy
from gt_model import *

def decode_eyeq4_bin_data(save_path):
    # 加载DBC文件
    db = database.load_file('eyeq4.dbc')
    messages = db.messages
    messages.sort(key=lambda x: x.frame_id)

    # 读入包含CAN信号的二进制文件
    with open('eyeq4.bin', 'rb') as f:
        data = f.read()
    # 遍历dbc message
    message_dict = {
        message.frame_id: {"name": message.name, "signal_names": [signal.name for signal in message.signals]} for
        message in messages}
    offset = 0
    messages_to_save = []

    save_object = collections.defaultdict(list)
    for frame_id, data_ in message_dict.items():
        types = ['timestamp'] + data_['signal_names']
        save_object[frame_id].append(types)

    while offset < len(data):
        # Extract the CAN ID and data from the binary frame
        time = struct.unpack("<Q", data[offset:offset + 8])[0]
        lenth = struct.unpack("B", data[offset + 8:offset + 9])[0]
        can_id = struct.unpack('I', data[offset + 9:offset + 13])[0]
        # if can_id != 1828:
        #     offset += 21 - 8 + lenth
        #     continue
        can_data = data[offset + 13:offset + 13 + lenth]
        # print("lenth:", lenth)
        # Look up the message definition in the DBC file
        if can_id in message_dict:
            x = db.decode_message(can_id, can_data)
            message = db.get_message_by_frame_id(can_id)

            # Parse each signal in the message and store the results in a dictionary
            signals = [int(time)]
            for signal in message.signals:
                signals.append(x[signal.name])
                # print(signal.name, physical_value)
            # Print the signals dictionary for debugging purposes
            messages_to_save.append({time: {"id": can_id, "signals": signals}})
            save_object[can_id].append(signals)
        # Increment the offset to move to the next CAN frame in the binary file
        # print(hex(message.frame_id), message.name)
        offset += 21 - 8 + lenth
        # if offset > 7000000:
        #     break
    for frame_id, data in save_object.items():
        message = db.get_message_by_frame_id(frame_id)
        if "_OBS_MSG" not in message.name: continue
        file_name = str(message.frame_id) + "_" + message.name + ".csv"
        file_name = os.path.join(save_path, file_name)
        if len(data) <= 500:
            print("====skip====")
            continue
        df = pd.DataFrame(data[500:],columns=data[0])
        df.to_csv(file_name,index= False,na_rep='NA')

def convert_csv_to_json(file_path):
    files = os.listdir(file_path)
    res = []
    for file in files:
        filename = os.path.join(file_path,file)
        df = pd.read_csv(filename)
        res.append(df.copy())
    if len(res)<1:return
    num = len(res[0])
    print(num)
    for i in range(num):
        data_new = copy.deepcopy(gt_model)
        filename = ''
        for item in res:
            timestamp = item.iloc[i,0]
            col_num = len(item.iloc[0])
            # 拷贝一份gt模板
            start = 1
            while start + 21 < col_num:
                item_3d["x"] = item.iloc[i, start + 15]
                item_3d["y"] = item.iloc[i, start + 14]

                if abs(item_3d["x"]) + abs(item_3d["y"]) > 0.05:
                    item_2d["type"] = item.iloc[i, start + 1].strip().strip("'")
                    x,y = world_2_uv((item_3d["x"],item_3d["y"]))
                    item_2d["x"] = x
                    item_2d["y"] = y
                    item_2d["width"] = 1000
                    item_2d["height"] = 1000
                    item_2d["id"] = int(item.iloc[i, start])
                    item_2d["cameraId"] = "front_near"
                    obstacle_context["2d"] = [item_2d]

                    item_3d["rel_vx"] = round(item.iloc[i, start + 17], 3)
                    item_3d["rel_vy"] = round(item.iloc[i, start + 16], 3)
                    item_3d["length"] = None
                    item_3d["width"] = item.iloc[i, start + 11]
                    item_3d["height"] = item.iloc[i, start + 12]
                    item_3d["yaw"] = round(item.iloc[i, start + 13] * np.pi / 180, 3)
                    item_3d['id'] = int(item.iloc[i, start])
                    item_3d['type'] = item.iloc[i, start + 1].strip().strip("'")
                    obstacle_context["3d"] = item_3d
                    data_new["obstacle"].append(copy.deepcopy(obstacle_context))
                if start < 21:
                    start += 21
                else:
                    start += 22
            if filename == '':
                filename = str(timestamp) + '.json'
            else:
                if filename[:-5] != str(timestamp):
                    print(filename[:-5],str(timestamp))
                    print(f'第{i}行有问题！')
        save_name = os.path.join("/home/cheng/data/mycode/perception-test/mobileeye/jsons", filename)
        with open(save_name,"w") as f:
            json.dump(data_new,f,indent=4)

def world_2_uv(world_point):
    x = world_point[0]
    y = world_point[1]
    z = 0.7
    world_p = np.array([x,y,z,1])
    # 相机外参:相机到车体，4x4旋转平移矩阵
    R = np.array([[-0.  ,-0.0008239203419564778,0.9999935694272383,2.09],
         [-0.9998964322674533,0.013965136104336242,-0.0034784640871957694,0],
         [-0.013962180323192191,-0.9999021432764598,-0.0008725776556789232,1.41],
         [0,0,0,1]])
    # 相机内参
    camera_in_params = np.array([[1010.2361246437642,0,971.524849288821,0],
                                 [0,1009.9933610930672,542.6131924168506,0],
                                 [0,0,1,0]])
    # 世界坐标系--转成-->像素坐标系
    uv_point = np.matmul(camera_in_params,np.matmul((np.linalg.inv(R)),world_p))
    x1,y1,z1 = uv_point.tolist()
    # if x1<0 or y1<0:
    #     return -1,-1
    return round(x1/z1,3),round(y1/z1,3)

convert_csv_to_json("/home/cheng/data/mycode/perception-test/mobileeye/result")