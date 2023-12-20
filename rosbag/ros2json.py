import rosbag
import os
import utils

def get_tsr_msg_tracks(msg):
    json_data_list =[]
    if msg.traffic_sign_list!=[]:
        for temp in msg.traffic_sign_list:
            obstacle_type = config.front_tsr["enum_obstacle"][temp.sub_sign_type]
            is_min = temp.speed_limit_type
            is_end = temp.speed_limit_switch
            is_led = temp.speed_limit_electric
            is_ring = temp.speed_limit_ring
            camera_id = temp.camera_position
            box_2d = {
                "x":temp.uv_bbox2d.left_top.x,
                "y":temp.uv_bbox2d.left_top.y,
                "w":temp.uv_bbox2d.size.x,
                "h":temp.uv_bbox2d.size.y
            }
            distance = {
                "x":temp.positionx,
                "y":temp.positiony
            }
            json_content = {
                "box_2d":box_2d,
                "distance":distance,
                "camera_id":camera_id,
                "obstacle_type":obstacle_type,
                "is_min":is_min,
                "is_end":is_end,
                "is_led":is_led,
                "is_ring":is_ring
            }
            json_data_list.append(json_content)
    return json_data_list

def get_bag_data(bag_file,dst,num):
    bag_data = rosbag.Bag(bag_file,'r')
    obstacle_data = bag_data.read_messages('/perception/traffic_signs')
    frame_id = num
    for topic,msg, t in obstacle_data:
        json_name = str(frame_id) + '.json'
        frame_id +=1
        json_data = get_tsr_msg_tracks(msg)
        utils.write_json_data(os.path.join(dst,json_name),json_data) 

bag_file = '/home/lixialin/Downloads/keshihua0905/2023-09-05/demo_byd-01_2023-09-05-16-52-48_0.bag'
dst = '/home/lixialin/Downloads/keshihua0905/2023-09-05'
os.makedirs(dst,exist_ok=True)
num = 0
num = get_bag_data(bag_file,dst,num)
