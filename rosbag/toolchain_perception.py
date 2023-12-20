import rosbag
import argparse
import os
import json


bag_file = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/06_data/result/fusion.bag'
bag_data = rosbag.Bag(bag_file,'r')
obstacle_data = bag_data.read_messages(["/perception/obstacle_list","/fusion/obstacle_list"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('perception_ros_path',type=str, help='标注文件路径')
    args = parser.parse_args()
    return args

def write_json_data(json_file,str_content):
    with open(json_file,'w')  as f:
        try:
            json.dump(str_content,f,indent=4)
        except:
            print('写入json内容失败')

def get_msg_tracks(msg):
    json_data_list =[]
    if msg.tracks!=[]:
        for temp in msg.tracks:
            type = temp.type
            camera_id = temp.camera_position
            box_2d = {
                "x":temp.uv_bbox2d.left_top.x,
                "y":temp.uv_bbox2d.left_top.y,
                "w":temp.uv_bbox2d.size.x,
                "h":temp.uv_bbox2d.size.y
            }
            distance = {
                "x":temp.position.x,
                "y":temp.position.y
            }
            box_3d = {
                "l":temp.bbox3d.size.x,
                "w":temp.bbox3d.size.y,
                "h":temp.bbox3d.size.z
            }
            # yaw = temp.rotation.yaw
            json_content = {
                "type":type,
                "box_2d":box_2d,
                "box_3d":box_3d,
                "distance":distance,
                # "yaw":yaw,
                "camera_id":camera_id
            }
            json_data_list.append(json_content)
    return json_data_list


def get_bag_data(bag_file,dst,num):
    frame_id = num
    for topic,msg, t in obstacle_data:
        json_name = str(frame_id) + '.json'
        frame_id +=1
        json_data = get_msg_tracks(msg)
        write_json_data(os.path.join(dst,json_name),json_data)

if __name__ == '__main__':
    args = parse_args()
    perception_ros_path = args.perception_ros_path
    obstacle_data = bag_data.read_messages('/perception/obstacle_list')
    num = 0
    bag = os.path.join(perception_ros_path,'perception.bag')
    dst = os.path.join(perception_ros_path,'perception_json')
    os.makedirs(dst,exist_ok=True)
    num = get_bag_data(bag,dst,num)
    

