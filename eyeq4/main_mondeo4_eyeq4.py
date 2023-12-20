from cantools import database
import time as tim
import struct
import collections
import os

def convert_signed_signal1(signal_value, start_bit, length, fmt):  # radar
    # 将信号值从二进制形式转换为十进制有符号整数形式
    signed_value = struct.unpack(">Q", signal_value)[0]
    r = bin(signed_value)
    # 根据信号位和长度确定信号值的位域，并将其右对齐
    byte_index = 7 - start_bit // 8
    res = start_bit % 8
    start_bit = byte_index * 8 + res
    start_bit -= length - 1
    
    
    mask = ((1 << length) - 1) << start_bit
    bitfield = (signed_value & mask) >> start_bit

    # 符号扩展
    if fmt == 'q' and bitfield & (1 << (length - 1)):
        bitfield -= 1 << length
    
    if fmt == 'd':  # 8 bytes float (double)
        print(123)
        return 0
        # raise Exception("double not support")
    
    # 返回转换后的整数值
    return bitfield
collect = collections.defaultdict(int)

def convert_signed_signal(signal_value, start_bit, length, fmt):
    # 将信号值从二进制形式转换为十进制有符号整数形式
    signed_value = struct.unpack("<Q", signal_value)[0]
    # 根据信号位和长度确定信号值的位域，并将其右对齐
    
    
    mask = ((1 << length) - 1) << start_bit
    bitfield = (signed_value & mask) >> start_bit

    # 符号扩展
    if fmt == 'q' and bitfield & (1 << (length - 1)):
        bitfield -= 1 << length
    
    if fmt == 'd':  # 8 bytes float (double)
        raise Exception("double not support")
    
    # 返回转换后的整数值
    return bitfield

def convert_signed_signal2(signal_value, start_bit, length, fmt, size):
    # 将信号值从二进制形式转换为十进制有符号整数形式
    start_bytes = start_bit // 8
    res = start_bit % 8
    end_bytes = (start_bit + length - 1) // 8 + 1
    signal_value = signal_value[start_bytes: end_bytes]
    fill = 0
    fill = fill.to_bytes(8, "little")
    signal_value = fill[0: 8 - (end_bytes - start_bytes)] + signal_value
    # 根据信号位和长度确定信号值的位域，并将其右对齐
    signed_value = struct.unpack(">" + fmt, signal_value)[0]
    mask = ((1 << length) - 1)
    # raise RuntimeError
    # TODO : 符号扩展
    # 符号扩展
    if fmt in ['q', 'Q']:
        return (signed_value >> res) & mask
    raise Exception("double not support")
    


# Load the DBC file
db = database.load_file('eyeq4.dbc')
messages = db.messages
messages.sort(key=lambda x: x.frame_id)
messages_used = []
# Open the binary file containing the CAN frames
with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/02_tools/nm_tools/eyeqq4/eyeq4.bin', 'rb') as f:
    data = f.read()
# print(data)
# Iterate over each CAN frame in the binary file
message_dict = {message.frame_id: {"name": message.name, "signal_names": [signal.name for signal in message.signals]} for message in db.messages}
offset = 0
messages_to_save = []
ty = tim.time()

save_object = collections.defaultdict(list)
for frame_id, data_ in message_dict.items():
    types = ['timestamp'] + data_['signal_names']
    save_object[frame_id].append(types)

while offset < len(data):
    # Extract the CAN ID and data from the binary frame
    time = struct.unpack("<Q", data[offset:offset + 8])[0]
    lenth = struct.unpack("B", data[offset + 8:offset + 9])[0]
    can_id = struct.unpack('I', data[offset + 9:offset+13])[0]
    # if can_id != 1828:
    #     offset += 21 - 8 + lenth
    #     continue
    can_data = data[offset+13:offset+13+lenth]
    print("lenth:", lenth)
    # print(tim.time() - ty, time)
    ty = tim.time()
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
    file_name = str(message.frame_id) + "_" + message.name
    file_name = os.path.join("./eyeq4/", file_name)
    if len(data) == 1:
        continue
    with open(file_name + ".csv", "w") as f:
        for line in data:
            f.write(str(line)[1:-1])
            f.write("\n")
