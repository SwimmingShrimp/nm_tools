'''
Author: lixialin lixialin@nullmax.ai
Date: 2023-12-20 14:14:05
LastEditors: lixialin lixialin@nullmax.ai
LastEditTime: 2024-09-10 14:35:27
'''
from cantools import database
import sys
sys.path.append("..")
import utils
import struct
import collections
import json
import pandas as pd

# Load the DBC file
db = database.load_file('/home/ubuntu/Music/dbc/GWM_PCAN_V2.6.dbc')
messages = db.messages
messages.sort(key=lambda x: x.frame_id)
messages_used = []
node_content_list = []
for node in db.nodes:
    node_content_list.append(node.name)
message_content = []
signal_content_dict = {}
for message in db.messages:
    message_content.append(message.name)
    if message=='Last_Ignition_Cycle_Fault_Table':
        continue
    signal_content = []
    for signal in message.signals:
        signal_name = signal.name

        if signal.choices:
            signal_values = repr(dict(signal.choices))
        else:
            signal_values = None
        signal_content.append([signal_name,signal_values])
    signal_content_dict[message.name] = signal_content


# 导出json
# json_data = {
#     "message":message_content,
#     "signal":signal_content_dict
# }
# json_path = '/home/ubuntu/Pictures/BTL.json'
# utils.write_json_data(json_path,json_data)

# 导出Excel
data1 = message_content
df = pd.DataFrame(data1)
df.to_excel('{}/{}.xlsx'.format('/home/ubuntu/Pictures','BTL'),sheet_name='message_names')
data2 = []
for key,value in signal_content_dict.items():
    message_name = key
    for value_ in value:
        item_name = value_[0]
        enumerate_value = value_[1]
        data2.append([message_name,item_name,enumerate_value])
col_names = ['message_name','itme_name','enumerate_value']
df2 = pd.DataFrame(data2)
with pd.ExcelWriter('{}/{}.xlsx'.format('/home/ubuntu/Pictures','BTL'),mode='a',engine='openpyxl') as writer:
    df2.to_excel(writer,sheet_name='details')

