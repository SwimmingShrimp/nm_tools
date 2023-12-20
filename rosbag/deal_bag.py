import rosbag
# import sys
# sys.path.append('..')
# import utils
# import os
# import pdb
# import yaml


bag_file = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/06_data/result/fusion.bag'
bag_data = rosbag.Bag(bag_file,'r')
obstacle_data = bag_data.read_messages(["/perception/obstacle_list","/fusion/obstacle_list"])
# obstacle_data = bag_data.read_messages('/perception/traffic_lights')
# obstacle_data = bag_data.read_messages('/perception/traffic_signs')
for topic,msg, t in obstacle_data:
    if msg is not None:
        print(msg,type(msg))

# 将内容写入csv文件            
# rostopic echo -b fusion.bag -p /fusion/obstacle_list > ./fusion.csv