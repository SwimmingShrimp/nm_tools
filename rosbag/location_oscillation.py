import rosbag
import os

rosbags_path = ''
rosbags_list = []
for rosbag_ in os.listdir(rosbags_path):
    if rosbag_.endswith('.bag'):
        rosbags_list.append(os.path.join(rosbags_path,rosbag_))

for rosbag_file in rosbags_list: