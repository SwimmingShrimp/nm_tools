import json
import os
import os.path as osp

import pandas as pd
from parse import parse

csv_path = "/home/sunhuibo/下载/nullmax_lane_log.csv"
output_json_dir = "/home/sunhuibo/下载/wukong_out_json/"
os.makedirs(output_json_dir, exist_ok=True)
odom_path = "/media/sunhuibo/data/Work/data/0907/update_vehicle.log"
odom_info = {}

pd_reader = pd.read_csv(csv_path)
min_frame_id, max_frame_id = 0, 0
lane_data = {}
for index, row in pd_reader.iterrows():
    frame_id = str(int(row["frame_id"]))
    if frame_id not in lane_data:
        lane_data[frame_id] = []
    # skip invalid lane
    if row['type_position'] == 8 or row['confidence'] == -1:
        continue
    lane_data[frame_id].append(row)
    int_frame_id = int(frame_id)
    if int_frame_id < min_frame_id:
        min_frame_id = int_frame_id
    if int_frame_id > max_frame_id:
        max_frame_id = int_frame_id

with open(odom_path, 'r') as odom_file:
    lines = odom_file.readlines()
    for line in lines:
        info = parse("speed = {speed} yaw_rate = {yaw_rate} steering_angle = {steering_angle} x = {x} y = {y} theta = {theta} frame_id = {frame_id}",
                     line.strip())
        if min_frame_id <= int(info['frame_id']) <= max_frame_id:
            odom_info[info['frame_id']] = info

for key in lane_data:
    frame_id = key
    int_frame_id = int(key)
    json_data = {}
    json_data["lane"] = []
    json_data['frame_id'] = int_frame_id
    if frame_id in odom_info:
        odom = odom_info[frame_id]
        json_data["odometry"] = {
            "x": float(odom["x"]),
            "y": float(odom["y"]),
            "z": float(odom["z"]),
            "theta": float(odom["theta"])
        }
    for lane in lane_data[key]:
        single_lane = {}
        single_lane['lane_type'] = lane["type_position"]

        all_pw = []
        for x in range(0, int(lane['end_longitudinal']), 2):
            y = float(lane['c0']) + (float(lane["c1"]) + (float(lane["c2"]) + float(lane["c3"]) * x) * x) * x
            lane_marker = {}
            lane_marker["id"] = x
            pre_id = x - 2
            suc_id = x + 2
            if x == 0:
                pre_id = -1
            if x + 2 > int(lane["end_longitudinal"]):
                suc_id = -2
            lane_marker["pre_id"] = pre_id
            lane_marker["suc_id"] = suc_id
            lane_marker["points"] = {}
            lane_marker["points"]["x"] = x
            lane_marker["points"]["y"] = -y
            lane_marker["points"]["z"] = 0
            all_pw.append(lane_marker)
        single_lane['feature'] = all_pw
        json_data["lane"].append(single_lane)

    with open(osp.join(output_json_dir, frame_id + '.json'), 'w') as json_file:
        json.dump(json_data, json_file)

