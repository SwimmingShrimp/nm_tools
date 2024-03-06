import os
import os.path as osp
import rosbag
import json
import sys
import pdb
sys.path.append("/home/data/workspace/AEB/code/demo/disk-packages/dist-packages")
sys.path.append("/home/data/workspace/AEB/code/demo/disk-packages/dist-packages/nullmax_msgs")
from nullmax_msgs.msg import CameraObstacleArray
from nullmax_msgs.msg import CameraObstacle
from replay_parser import generate_vehicle_state
import copy

def check_exist_or_mkdir(dir_path):
    if not osp.exists(dir_path):
        os.makedirs(dir_path)


def modify_video_path_in_json(json_file, new_value):
    # 打开JSON文件并将其加载为Python对象
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 修改"detect_by_video"的值
    data['offline']["image_root"] = new_value

    # 保存修改后的数据到文件中
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def modify_index_in_json(json_file, start_index, end_index):
    # 打开JSON文件并将其加载为Python对象
    with open(json_file, 'r') as f:
        data = json.load(f)

    # 修改"detect_by_video"的值
    data['offline']['start_index'] = int(start_index.strip())
    data['offline']['finish_index'] = int(end_index.strip())

    # 保存修改后的数据到文件中
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def find_timestamp_in_dir(dir_path, time_stamp):
    video_path = ""
    frame_id   = -1
    for d_root, dirs, files in os.walk(dir_path):
        if "timestamp.log" in files and  "sys_state.log" in files:
            with open(osp.join(d_root, "timestamp.log" ), 'r') as f:
                for line in f.readlines():
                    if str(time_stamp) in line:
                        video_path = d_root
                        frame_id  = line.strip().split(" ")[1]
                        break
    return video_path, frame_id

def convert_264file2image(dir_path, cut_video_file_path):
    cp_cmd = "cp {} {}"
    sh_cmd = "sh {}"    

    if not osp.exists(osp.join(dir_path, "images")):
        tmp_cp_cmd = cp_cmd.format(cut_video_file_path, dir_path)
        if not osp.exists(osp.join(dir_path, "cut_video.sh")):
            os.system(tmp_cp_cmd)
        os.chdir(dir_path)
        print("Start to cut video {} images".format(dir_path))
        tmp_sh_cmd = sh_cmd.format("cut_video.sh")
        os.system(tmp_sh_cmd)
        print("CP timestamp.log to images")
        tmp_cp_cmd = cp_cmd.format(osp.join(dir_path, "timestamp.log"), osp.join(dir_path, "images"))
        os.system(tmp_cp_cmd)
        # ## 从bag中生成新的包含每一帧自车状态的vehicle_state
        # generate_vehicle_state(bag_path,osp.join(dir_path, "timestamp.log"),osp.join(dir_path, "images/vehicle_state.log"))

        # print("CP vehicle_state.log to images")
        # tmp_cp_cmd = cp_cmd.format(osp.join(dir_path, "vehicle_state.log"), osp.join(dir_path, "images"))
        # os.system(tmp_cp_cmd)
    else:
        print("Exists {}".format(osp.join(dir_path, "images")))

# 自动执行obstacle_perception 
def launch_obstacle_perception(bag_name, obstacle_perception_dir, obstacle_perception_json_path, save_path):
    os.chdir(obstacle_perception_dir)
    # export_cmd = "source ../export_x86_linux.sh"
    # os.system(export_cmd)
    launch_obstacle_perception_cmd = "./build_infer/x86_linux/obstacle_inference_main {} >> {}.txt"
    mv_cmd = "mv {} {}"
    print("Start to run obstacle {}".format(obstacle_perception_json_path))
    launch_obstacle_perception_cmd_tmp = launch_obstacle_perception_cmd.format(obstacle_perception_json_path, bag_name)
    os.system(launch_obstacle_perception_cmd_tmp)
    check_exist_or_mkdir(osp.join(save_path, bag_name))
    print("Start to move image_record {}".format(osp.join(save_path, bag_name)))
    mv_cmd_tmp = mv_cmd.format("image_record", osp.join(save_path, bag_name))
    os.system(mv_cmd_tmp)

def read_timestamp_from_rosbag(rosbag_path):
    time_stamp = 0
    bag_data = rosbag.Bag(rosbag_path)
    cnt = 0
    start_timestamp = -1
    end_timestamp = -1
    for topic, msg, t in bag_data.read_messages():
        if topic == "/perception/obstacle_list":
            time_seq = msg.header.seq
            time_nsec = msg.header.stamp.secs* 1000000000 + msg.header.stamp.nsecs
            time_stamp = int(time_nsec / 1000)
            if cnt == 0:
                start_timestamp = time_stamp
            end_timestamp = time_stamp
            cnt += 1
    return start_timestamp, end_timestamp

def read_json(file):
    with open(file,'r') as f:
        data = json.load(f)
        camera_fusion = data[8]['camera_fusion']
    return camera_fusion

def process_all_tracker(path):
    file_list =get_json_file_list(path)
    timestamp_trackers = dict()
    for file in file_list:
        json_data = read_json(file)
        timestamp = json_data['timestamp']
        timestamp_trackers[timestamp] = dict()
        timestamp_trackers[timestamp]['cipv_id'] = json_data['cipv_id']
        timestamp_trackers[timestamp]['cipv_status'] = json_data['cipv_status']
        timestamp_trackers[timestamp]['tracks'] = json_data['tracks']
        
    return timestamp_trackers

def get_json_file_list(path):
    file_list = []
    for file in sorted(os.listdir(path)):
        if file[0]=='.':
            continue
        file_path = os.path.join(path,file)
        file_list.append(file_path)
    return file_list

def generate_obstacle_perception_topic(msg, obstacle_inf_dict):
    should_break = False

    time_seq = msg.header.seq
    time_nsec = msg.header.stamp.secs* 1000000000 + msg.header.stamp.nsecs
    time_stamp = int(time_nsec / 1000)
    camera_obstacle_array = CameraObstacleArray()
    camera_obstacle_array.header = msg.header
    camera_obstacle_array.send_time = msg.send_time
    camera_obstacle_array.camera_id = msg.camera_id
    camera_obstacle_array.cipv_id = 0
    camera_obstacle_array.cipv_exist = 0
    camera_obstacle_array.cciv_id = msg.cciv_id
    camera_obstacle_array.cciv_direction = msg.cciv_direction
    if time_stamp not in obstacle_inf_dict.keys():
        camera_obstacle_array.tracks = []
        print("{} not in obstacle_inf_dict".format(time_stamp))
        should_break = True
    else:
        new_tracks = obstacle_inf_dict[time_stamp]
        camera_obstacle = CameraObstacle()
        camera_obstacle_array.cipv_id = new_tracks['cipv_id']
        camera_obstacle_array.cipv_exist = new_tracks['cipv_status']
        if new_tracks['tracks'] == None:
            camera_obstacle_array.tracks = []
        else:
            for track in new_tracks['tracks']:
                camera_obstacle.id = track['obstacle_id']
                camera_obstacle.age = track['obstacle_age']
                camera_obstacle.position.x = track['position']['obstacle_pos_x_filter']
                camera_obstacle.position.y = track['position']['obstacle_pos_y_filter']
                camera_obstacle.position_std.x = track['position_std']['obstacle_std_pos_x_filter']
                camera_obstacle.position_std.y = track['position_std']['obstacle_std_pos_y_filter']
                camera_obstacle.velocity.x = track['velocity']['obstacle_rel_vel_x_filter']
                camera_obstacle.velocity.y = track['velocity']['obstacle_rel_vel_y_filter']
                camera_obstacle.velocity_std.x = track['velocity_std']['obstacle_std_rel_vel_x_filter']
                camera_obstacle.velocity_std.y = track['velocity_std']['obstacle_std_rel_vel_y_filter']
                camera_obstacle.accel.x = track['accel']['obstacle_rel_acc_x_filter']
                camera_obstacle.accel.y = track['accel']['obstacle_rel_acc_y_filter']
                camera_obstacle.accel_std.x = track['accel_std']['obstacle_std_rel_acc_x_filter']
                camera_obstacle.accel_std.y = track['accel_std']['obstacle_std_rel_acc_y_filter']
                camera_obstacle.bbox3d.center.x = 0
                camera_obstacle.bbox3d.center.y = 0
                camera_obstacle.bbox3d.center.z = 0
                camera_obstacle.bbox3d.size.x= track["obstacle_height"]
                camera_obstacle.bbox3d.size.y = track["obstacle_width"]
                camera_obstacle.bbox3d.size.z = track["obstacle_length"]
                camera_obstacle.uv_bbox2d.left_top.x= track['uv_bbox2d']['obstacle_bbox.x']
                camera_obstacle.uv_bbox2d.left_top.y = track['uv_bbox2d']['obstacle_bbox.y']
                camera_obstacle.uv_bbox2d.size.x = track['uv_bbox2d']['obstacle_bbox.width']
                camera_obstacle.uv_bbox2d.size.y= track['uv_bbox2d']['obstacle_bbox.height']
                camera_obstacle.blinker_info = 1
                camera_obstacle.cut_in_and_out = track['cut_in_and_out']
                camera_obstacle.cut_direction = track['cut_direction']
                camera_obstacle.cut_in_prob = 0.0
                camera_obstacle.lane = track['obstacle_lane']
                camera_obstacle.status = track['obstacle_status']
                camera_obstacle.type = track['obstacle_type']
                camera_obstacle.ttc = track['obstacle_ttc']
                camera_obstacle.uv_dis_to_line = 1023
                camera_obstacle.uv_lane_width = 1024
                camera_obstacle.brake_lights = track['obstacle_brake_lights']
                camera_obstacle.valid = track['obstacle_valid']
                camera_obstacle.type_confidence = track['obstacle_type_confidence']
                camera_obstacle.exist_prob = track['obstacle_exist_prob']
                camera_obstacle.rotation.roll  = 0.0
                camera_obstacle.rotation.pitch  = 0.0
                camera_obstacle.rotation.yaw  = 0.0
                camera_obstacle.corners.corn_lf.x   = 0.0
                camera_obstacle.corners.corn_lf.y   = 0.0
                camera_obstacle.corners.corn_rf.x   = 0.0
                camera_obstacle.corners.corn_rf.y   = 0.0
                camera_obstacle.corners.corn_lr.x   = 0.0
                camera_obstacle.corners.corn_lr.y   = 0.0
                camera_obstacle.corners.corn_rr.x   = 0.0
                camera_obstacle.corners.corn_rr.y   = 0.0
                camera_obstacle.camera_position = track['camera_ids'][-1]
                camera_obstacle.aeb_valid = track['aeb_valid']
                camera_obstacle.fcw_valid = track['fcw_valid']
                camera_obstacle_array.tracks.append(copy.deepcopy(camera_obstacle))
    return camera_obstacle_array, should_break
        

def generate_new_bag(in_bagfile, obstacle_inf_dict, output_bag_path):
    cnt = 0
    with rosbag.Bag(output_bag_path, 'w') as output_bag_file:
        for topic, msg, t in in_bagfile.read_messages():
            if topic == "/perception/obstacle_list":
                msg, should_break = generate_obstacle_perception_topic(msg, obstacle_inf_dict)
                if should_break:
                    cnt += 1
                    if cnt > 10:
                        break
                output_bag_file.write(topic, msg, t)
            else:
                output_bag_file.write(topic, msg, t)
        output_bag_file.close()
    in_bagfile.close()

def fushion_nb2bag(dir_path):
    nullmax_pilot_dir = "/workspace/nullmax_workspace/code_pro/nullmax_pilot"
    os.chdir(nullmax_pilot_dir)
    convert_cmd = "bash ./scripts/offline_test.sh {}"
    for d_root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".bag"):
                convert_cmd_tmp = convert_cmd.format(osp.join(d_root, file))
                print("Start to try to convert {}".format(osp.join(d_root, file)))
                os.system(convert_cmd_tmp)

if __name__ == '__main__':
    dir_path = "/media/ubuntu/datacycle10/2023_beijing"
    cut_video_file_path = "/home/data/workspace/AEB/code/demo/cut_video.sh"
    bag_list = [
#         "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-50-1_chery-01_2023-04-24-17-22-31_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-3_chery-01_2023-04-24-14-33-57_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-60-2_chery-01_2023-04-24-15-21-42_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-30-1_chery-01_2023-04-24-13-51-26_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-3_chery-01_2023-04-24-14-44-29_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-30-1_chery-01_2023-04-24-17-13-07_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-5_chery-01_2023-04-24-15-06-08_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-1_chery-01_2023-04-24-14-48-51_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-60-3_chery-01_2023-04-24-16-31-25_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-40-1_chery-01_2023-04-24-16-14-47_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-20-2_chery-01_2023-04-24-13-49-54_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-1_chery-01_2023-04-24-17-03-01_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-40-1_chery-01_2023-04-24-17-17-20_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-4_chery-01_2023-04-24-16-10-26_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-2_chery-01_2023-04-24-14-42-47_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-40-3_chery-01_2023-04-24-16-18-59_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-2_chery-01_2023-04-24-15-37-31_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-1_chery-01_2023-04-24-14-37-25_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-2_chery-01_2023-04-24-14-50-24_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-50-2_chery-01_2023-04-24-14-09-34_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-40-2_chery-01_2023-04-24-17-20-12_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-50-2_chery-01_2023-04-24-15-16-54_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-1_chery-01_2023-04-24-13-54-30_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-60-2_chery-01_2023-04-24-14-22-11_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-5_chery-01_2023-04-24-16-12-30_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-60-1_chery-01_2023-04-24-15-18-52_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-20-1_chery-01_2023-04-24-13-48-04_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-30-2_chery-01_2023-04-24-17-15-31_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-50-1_chery-01_2023-04-24-16-20-58_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-60-3_chery-01_2023-04-24-14-24-05_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-1_chery-01_2023-04-24-14-30-12_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-2_chery-01_2023-04-24-17-09-21_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-4_chery-01_2023-04-24-14-06-14_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-60-2_chery-01_2023-04-24-16-27-14_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-4_chery-01_2023-04-24-15-05-00_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-4_chery-01_2023-04-24-14-35-40_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-2_chery-01_2023-04-24-13-56-03_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-50-1_chery-01_2023-04-24-15-15-07_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-3_chery-01_2023-04-24-16-08-17_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-3_chery-01_2023-04-24-15-03-26_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-50-1_chery-01_2023-04-24-14-07-47_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-60-1_chery-01_2023-04-24-16-24-32_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-1_chery-01_2023-04-24-15-32-19_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-30-2_chery-01_2023-04-24-13-52-50_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-60-1_chery-01_2023-04-24-14-11-34_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-2_chery-01_2023-04-24-14-32-09_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-3_chery-01_2023-04-24-13-57-38_0.bag",
# # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-50-2_chery-01_2023-04-24-16-22-46_0.bag",
# "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-1_chery-01_2023-04-24-16-59-15_0.bag",

        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-40-2_chery-01_2023-04-24-16-16-56_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-60-3_chery-01_2023-04-24-16-31-25_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-40-1_chery-01_2023-04-24-16-14-47_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-4_chery-01_2023-04-24-16-10-26_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-40-3_chery-01_2023-04-24-16-18-59_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-2_chery-01_2023-04-24-15-37-31_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-5_chery-01_2023-04-24-16-12-30_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-50-1_chery-01_2023-04-24-16-20-58_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-60-2_chery-01_2023-04-24-16-27-14_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-30-3_chery-01_2023-04-24-16-08-17_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CSFA-50%-50-2_chery-01_2023-04-24-16-22-46_0.bag",

        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-40-3_chery-01_2023-04-24-10-43-55_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-30-1_chery-01_2023-04-24-10-35-31_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-40-2_chery-01_2023-04-24-10-41-51_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-20-1_chery-01_2023-04-24-10-30-05_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-20-2_chery-01_2023-04-24-10-32-42_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-30-2_chery-01_2023-04-24-10-37-43_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-50-1_chery-01_2023-04-24-10-46-05_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-40-1_chery-01_2023-04-24-10-39-51_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-60-2_chery-01_2023-04-24-10-54-38_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-50-2_chery-01_2023-04-24-10-48-17_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cbna-50%-60-1_chery-01_2023-04-24-10-52-36_0.bag",

        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-2_chery-01_2023-04-24-11-34-34_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-30-2_chery-01_2023-04-24-11-51-04_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-2_chery-01_2023-04-24-12-01-35_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-30-1_chery-01_2023-04-24-11-14-46_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-1_chery-01_2023-04-24-11-04-36_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-30-1_chery-01_2023-04-24-11-49-30_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-50-1_chery-01_2023-04-24-11-56-17_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-2_chery-01_2023-04-24-11-07-01_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-1_chery-01_2023-04-24-11-59-53_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-2_chery-01_2023-04-24-11-20-01_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-40-2_chery-01_2023-04-24-11-54-24_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-3_chery-01_2023-04-24-11-47-48_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-3_chery-01_2023-04-24-12-04-14_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-3_chery-01_2023-04-24-11-39-39_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-3_chery-01_2023-04-24-11-12-38_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-3_chery-01_2023-04-24-11-22-34_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-40-1_chery-01_2023-04-24-11-52-43_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-1_chery-01_2023-04-24-11-43-12_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-30-2_chery-01_2023-04-24-11-16-21_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-50-1_chery-01_2023-04-24-11-25-26_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-1_chery-01_2023-04-24-11-30-50_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-1_chery-01_2023-04-24-11-18-09_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-50-2_chery-01_2023-04-24-11-28-37_0.bag",
         "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-50-2_chery-01_2023-04-24-11-58-08_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-2_chery-01_2023-04-24-11-45-51_0.bag",

        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-40-2_chery-01_2023-04-25-11-23-32_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-50-3-right_chery-01_2023-04-25-11-38-58_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-60-2-left_chery-01_2023-04-25-11-47-17_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/demo_chery-01_2023-04-25-11-06-22_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrs-40-left-3_chery-01_2023-04-25-11-10-02_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-50-4-right_chery-01_2023-04-25-11-41-04_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-30-1_chery-01_2023-04-25-11-18-35_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-left-80-4_chery-01_2023-04-25-12-09-18_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-70-2_chery-01_2023-04-25-11-57-14_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-70-1_chery-01_2023-04-25-11-54-21_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-left-80-3_chery-01_2023-04-25-12-07-22_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-80-2_chery-01_2023-04-25-12-05-26_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-60-4_chery-01_2023-04-25-11-52-04_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrs-40-left-2_chery-01_2023-04-25-11-07-12_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-80-1_chery-01_2023-04-25-12-03-29_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-40-4-left_chery-01_2023-04-25-11-36-25_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-40-3-left_chery-01_2023-04-25-11-34-20_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-right-70-3_chery-01_2023-04-25-11-59-14_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-100%-60-3_chery-01_2023-04-25-11-49-22_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-40-1_chery-01_2023-04-25-11-20-54_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-60-1-left_chery-01_2023-04-25-11-45-12_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-50-1_chery-01_2023-04-25-11-28-15_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrs-100%-30-4_chery-01_2023-04-25-11-12-45_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-fcw-right-70-4_chery-01_2023-04-25-12-01-16_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-50-2_chery-01_2023-04-25-11-32-16_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrs-100%-30-3_chery-01_2023-04-25-11-11-17_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-25-morning/ccrm-100%-40-3_chery-01_2023-04-25-11-25-46_0.bag",

        ]

    bag_list_test = [
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-30-1_chery-01_2023-04-24-17-13-07_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-1_chery-01_2023-04-24-17-03-01_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-40-1_chery-01_2023-04-24-17-17-20_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-40-2_chery-01_2023-04-24-17-20-12_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-30-2_chery-01_2023-04-24-17-15-31_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-2_chery-01_2023-04-24-17-09-21_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-20-1_chery-01_2023-04-24-16-59-15_0.bag",
        # "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CBLA-50%-50-1_chery-01_2023-04-24-17-22-31_0.bag",

        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-2_chery-01_2023-04-24-11-34-34_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-30-2_chery-01_2023-04-24-11-51-04_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-2_chery-01_2023-04-24-12-01-35_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-30-1_chery-01_2023-04-24-11-14-46_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-1_chery-01_2023-04-24-11-04-36_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-30-1_chery-01_2023-04-24-11-49-30_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-50-1_chery-01_2023-04-24-11-56-17_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-2_chery-01_2023-04-24-11-07-01_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-1_chery-01_2023-04-24-11-59-53_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-2_chery-01_2023-04-24-11-20-01_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-40-2_chery-01_2023-04-24-11-54-24_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-3_chery-01_2023-04-24-11-47-48_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-60-3_chery-01_2023-04-24-12-04-14_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-3_chery-01_2023-04-24-11-39-39_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-20-3_chery-01_2023-04-24-11-12-38_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-3_chery-01_2023-04-24-11-22-34_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-40-1_chery-01_2023-04-24-11-52-43_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-1_chery-01_2023-04-24-11-43-12_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-30-2_chery-01_2023-04-24-11-16-21_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-50-1_chery-01_2023-04-24-11-25-26_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-60-1_chery-01_2023-04-24-11-30-50_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-40-1_chery-01_2023-04-24-11-18-09_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-25%-50-2_chery-01_2023-04-24-11-28-37_0.bag",
         "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-50-2_chery-01_2023-04-24-11-58-08_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-morning/cpna-75%-20-2_chery-01_2023-04-24-11-45-51_0.bag",

        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-3_chery-01_2023-04-24-14-33-57_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-60-2_chery-01_2023-04-24-15-21-42_0.bag",
        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-3_chery-01_2023-04-24-14-44-29_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-5_chery-01_2023-04-24-15-06-08_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-1_chery-01_2023-04-24-14-48-51_0.bag",
       
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-2_chery-01_2023-04-24-14-42-47_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-30-1_chery-01_2023-04-24-14-37-25_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-2_chery-01_2023-04-24-14-50-24_0.bag",
       
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-50-2_chery-01_2023-04-24-15-16-54_0.bag",
        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-60-1_chery-01_2023-04-24-15-18-52_0.bag",
        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-4_chery-01_2023-04-24-15-05-00_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-4_chery-01_2023-04-24-14-35-40_0.bag",
        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-50-1_chery-01_2023-04-24-15-15-07_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-40-3_chery-01_2023-04-24-15-03-26_0.bag",
        
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-25%-20-2_chery-01_2023-04-24-14-32-09_0.bag",

        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-3_chery-01_2023-04-24-13-57-38_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-30-1_chery-01_2023-04-24-13-51-26_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-20-2_chery-01_2023-04-24-13-49-54_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-50-2_chery-01_2023-04-24-14-09-34_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-1_chery-01_2023-04-24-13-54-30_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-60-2_chery-01_2023-04-24-14-22-11_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-20-1_chery-01_2023-04-24-13-48-04_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-4_chery-01_2023-04-24-14-06-14_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-40-2_chery-01_2023-04-24-13-56-03_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-50-1_chery-01_2023-04-24-14-07-47_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-30-2_chery-01_2023-04-24-13-52-50_0.bag",
        "/media/ubuntu/datacycle10/2023_beijing/2023-04-24-afternoon/CPFA-50%-60-1_chery-01_2023-04-24-14-11-34_0.bag",
        ]
    obstacle_perception_dir = "/home/ubuntu/project/obstacle_perception"
    obstacle_perception_json_file = "/home/ubuntu/project/obstacle_perception/data/obstacle_perception_tmp.json"
    fail_case = []
    # step 1
    for bag_path in bag_list_test:
        bag_name = osp.basename(bag_path)
        bag_name = os.path.splitext(bag_name)[0]
        print("Start to analysis {}".format(bag_path))
        print("Try to get start_timestamp and end_timestamp")
        start_timestamp, end_timestamp = read_timestamp_from_rosbag(bag_path)
        video_path1, start_index = find_timestamp_in_dir(dir_path, start_timestamp)
        video_path2, end_index = find_timestamp_in_dir(dir_path, end_timestamp)
        if video_path1 == "":
            fail_case.append(bag_name)
            print("not find timestamp in dir {}".format(start_index))
            continue
        # if video_path1 = video_path2:continue
        # print(video_path2,video_path1)
        if video_path1 != video_path2:
            fail_case.append(bag_name)
            print(" {} video_path1 != video_path2".format(bag_name))
            continue
        
        if osp.exists(osp.join(video_path1, bag_name, "image_record")):
            print("Exists {} image_record".format(bag_name))
            continue
        convert_264file2image(video_path1, cut_video_file_path)
        generate_vehicle_state(bag_path,osp.join(video_path1, "timestamp.log"),osp.join(video_path1, "images/vehicle_state.log"))
        

        cp_cmd = "cp {} {}"
        new_obstacle_perception_json_file = obstacle_perception_json_file.replace("obstacle_perception_tmp", "obstacle_perception_"+ bag_name)
        tmp_cp_cmd = cp_cmd.format(obstacle_perception_json_file, new_obstacle_perception_json_file)
        os.system(tmp_cp_cmd)
        modify_video_path_in_json(new_obstacle_perception_json_file, osp.join(video_path1, "images"))
        modify_index_in_json(new_obstacle_perception_json_file, start_index, end_index)

        launch_obstacle_perception(bag_name, obstacle_perception_dir, new_obstacle_perception_json_file, video_path1)


    for case in fail_case:
        print("{} failed".format(case))

    # # step 2
    # fail_case = []
    # for bag_path in bag_list:
    #     bag_name = osp.basename(bag_path)
    #     bag_name = os.path.splitext(bag_name)[0]
    #     start_timestamp, end_timestamp = read_timestamp_from_rosbag(bag_path)
    #     video_path, start_index = find_timestamp_in_dir(dir_path, start_timestamp)

    #     if not osp.exists(osp.join(video_path, bag_name, "image_record")):
    #         print("Not Exists {} image_record".format(bag_name))
    #         fail_case.append(bag_name)
    #         continue
    #     print("Start to generate bag_name to {}".format(osp.join(video_path, bag_name, "image_record")))
    #     json_dir_path = osp.join(video_path, bag_name, "image_record", "image_record_json", "camera_fusion")
    #     obstacle_inf_dict = process_all_tracker(json_dir_path)

    #     old_bag_data = rosbag.Bag(bag_path)
    #     save_bag_path = osp.join(video_path, bag_name, bag_name + ".bag")
    #     generate_new_bag(old_bag_data, obstacle_inf_dict, save_bag_path)


    # for case in fail_case:
    #     print("{} failed".format(case))

    # # step 3
    # cp_cmd = "cp {} {}"
    # for bag_path in bag_list:
    #     bag_name = osp.basename(bag_path)
    #     bag_name = os.path.splitext(bag_name)[0]
    #     start_timestamp, end_timestamp = read_timestamp_from_rosbag(bag_path)
    #     video_path, start_index = find_timestamp_in_dir(dir_path, start_timestamp)

    #     if not osp.exists(osp.join(video_path, bag_name, "image_record")):
    #         print("Not Exists {} image_record".format(bag_name))
    #         fail_case.append(bag_name)
    #         continue
    #     print("Start to mv bag_name to {}".format(osp.join(video_path, bag_name, "image_record")))

    #     gen_bag_path = osp.join(video_path, bag_name, bag_name + ".bag")
    #     save_path = "/media/ubuntu/datacycle10/2023_beijing/new_bag"
    #     tmp_cp_cmd = cp_cmd.format(gen_bag_path, save_path)
    #     os.system(tmp_cp_cmd)


    # for case in fail_case:
    #     print("{} failed".format(case))

    # step 4
    # dir_path = "/workspace/nullmax_workspace/scene_data/Chery-AEB/to_liqianle"
    # # fushion_nb2bag(dir_path)
    # dir_path = "/workspace/nullmax_workspace/scene_data/Chery-AEB/to_liqianle_second"
    # fushion_nb2bag(dir_path)


    # give ori bag to zesong
    # cp_cmd = "cp {} {}"
    # save_path_zs = "/workspace/nullmax_workspace/scene_data/Chery-AEB/to_zesong"
    # for bag_path in bag_list:
    #     tmp_cp_cmd = cp_cmd.format(bag_path, save_path_zs)
    #     os.system(tmp_cp_cmd)