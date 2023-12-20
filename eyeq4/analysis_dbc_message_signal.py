from cantools import database
import sys
sys.path.append("..")
import utils
import struct
import collections
import json

# Load the DBC file
db = database.load_file('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/02_tools/nm_tools/eyeq4/fov52_dbc/FCAN.dbc')
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
    signal_content = []
    for signal in message.signals:
        signal_name = signal.name

        if signal.choices:
            signal_values = repr(dict(signal.choices))
        else:
            signal_values = None
        signal_content.append([signal_name,signal_values])
    signal_content_dict[message.name] = signal_content



json_data = {
    "message":message_content,
    "signal":signal_content_dict
}
json_path = '/home/lixialin/Pictures/fov52-FCAN.json'
utils.write_json_data(json_path,json_data)
