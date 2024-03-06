# 将eyeq.bin的二进制文件根据不同信号解析成csv文件
from cantools import database
import shutil
import os
import argparse
import collections
import struct
import pandas as pd

def main():
    # 加载dbc
    db = database.load_file(dbc_file)
    messages = db.messages
    messages.sort(key=lambda x:x.frame_id)
    # 遍历dbc message
    message_dict = {
        message.frame_id:{
            "name":message.name,
            "signal_names":[signal.name for signal in message.signals]
        }
        for message in messages
    }
    # 获取csv文件头
    bin_decode_result = collections.defaultdict(list)
    for frame_id,data in message_dict.items():
        bin_decode_result[frame_id] = [['timestamp'] + data['signal_names']]
    # 读取bin文件
    with open(bin_file,'rb') as f:
        data = f.read()
    # 将bin文件解析结果保存到字典中
    offset = 0
    while offset < len(data):
        time = struct.unpack("<Q", data[offset:offset + 8])[0]
        lenth = struct.unpack("B", data[offset + 8:offset + 9])[0]
        can_id = struct.unpack('I', data[offset + 9:offset + 13])[0]
        can_data = data[offset + 13:offset + 13 + lenth]
        if can_id in message_dict:
            # 根据can_id获取message
            message = db.get_message_by_frame_id(can_id)
            # 解析can报文.If decode_choices is False scaled values are not converted to choice strings (if available).
            can_decode_data = db.decode_message(can_id,can_data, decode_choices=False)
            signal_dict = {signal.name: signal.choices for signal in message.signals}
            for key, value in can_decode_data.items():
                if signal_dict[key]:
                    if can_decode_data[key] in signal_dict[key]:
                        can_decode_data[key] = signal_dict[key][can_decode_data[key]]
            # 获取can报文中的结果[时间戳+所有信号的结果]
            signals = [int(time)]
            for signal in message.signals:
                signals.append(can_decode_data[signal.name])
            bin_decode_result[can_id].append(signals)
        offset += (13 + lenth)
    # 将字典中的结果保存到csv中
    for frame_id,data in bin_decode_result.items():
        file_name = str(frame_id) + '_' + message_dict[frame_id]['name'] + '.csv'
        file_path = os.path.join(csv_path, file_name)
        # 数据录制时，车道线有缓存，刚开始录制的是缓存数据，所以做一个过滤
        if len(data) <=500:
            print("====skip====")
            continue
        df = pd.DataFrame(data[500:],columns=data[0])
        df.to_csv(file_path,index= False,na_rep='NA')

if __name__=='__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('bin_path', type=str,help='the path of the eyeq4 bin file')
    # parser.add_argument('csv_path', type=str,help='the path of bin analyze files')
    # args = parser.parse_args()

    # bin_file = args.bin_path
    # csv_path = args.csv_path
    bin_file = '/home/lixialin/Pictures/mount_point/raw_data/eyeq4.bin'
    csv_path = '/home/lixialin/Pictures/csv_file'
    dbc_file = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/projects/nm_tools/eyeq4/fov100_2023_dbc/eyeq4.dbc'
    
    if os.path.exists(csv_path):
        shutil.rmtree(csv_path)
    os.makedirs(csv_path)
    main()