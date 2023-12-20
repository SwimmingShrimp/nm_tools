import rosbag
import os
import shutil
import rospy
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.transform import Rotation as R


def write_json_data(json_file,str_content):
    with open(json_file,'w')  as f:
        try:
            json.dump(str_content,f,indent=4)
        except:
            print('写入json内容失败')

def get_json_data(json_file):
    with open(json_file) as f:
        try:
            json_data = json.load(f)
        except:
            print('获取json文件内容失败')
        return json_data

def draw_pic_postion(dist_slam_list,dist_odom_list,agl_deg_slam_list,agl_deg_odom_list,pics_path,xlabel):
    x  = [m for m in range(len(dist_slam_list))]
    plt.figure(figsize=(18,10))
    plt.subplot(2,1,1)
    y_max = math.ceil(max(max(dist_slam_list),max(dist_odom_list))) +1
    plt.yticks([m for m in range(0,y_max)])
    plt.plot(x,dist_slam_list,label='slam_dist')
    plt.plot(x,dist_odom_list,label='odom_dist')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel("Distance(cm)")
    plt.title("The distance between calculate point and actual point")
    plt.grid(alpha=0.3)
    plt.subplots_adjust(hspace=0.3)
    plt.subplot(2,1,2)
    plt.yticks(([m/100 for m in range(-30,30)]))
    plt.plot(x,agl_deg_slam_list,label='slam_angle')
    plt.plot(x,agl_deg_odom_list,label='odom_angle')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel("Yaw(°)")
    plt.title("The yaw angle between calculate point and actual point")
    plt.grid(alpha=0.3)
    # plt.show()
    plt.savefig(os.path.join(pics_path,xlabel + '.png'))


def analyze_ros_2_json(rosbag_file,ros_2_jsons_path):
    slampose_topic = "/localization/vslam_posestamped_with_covariance"
    odom_topic = "/odom/current_pose"
    imu_whlspd_topic = "/control/twist"
    bag_data = rosbag.Bag(rosbag_file,'r')
    slampose,odom,whlspd = [],[],[]
    for topic,msg,t in bag_data.read_messages(slampose_topic):
        slampose.append([rospy.Time.to_nsec(t),msg])
    for topic,msg,t in bag_data.read_messages(odom_topic):
        odom.append([rospy.Time.to_nsec(t),msg])
    for topic,msg,t in bag_data.read_messages(imu_whlspd_topic):
        whlspd.append([rospy.Time.to_nsec(t),msg])
    # 根据SLAM的结果的时间取odom最近时间戳
    odom_new = []
    for idx,msg in enumerate(slampose):
        diff = abs(slampose[0][0] - odom[0][0])
        new_idx = idx
        for i in range(len(odom)):
            diff_new = abs(slampose[idx][0] - odom[i][0])
            if diff_new < diff:
                new_idx = i
                diff = diff_new
        odom_new.append(odom[new_idx])
    # 根据SLAM的结果的时间取whlspd最近时间戳
    whlspd_new = []
    for idx,msg in enumerate(slampose):
        diff = abs(slampose[0][0] - whlspd[0][0])
        new_idx = idx
        for i in range(len(whlspd)):
            diff_new = abs(slampose[idx][0] - whlspd[i][0])
            if diff_new < diff:
                new_idx = i
                diff = diff_new
        whlspd_new.append(whlspd[new_idx])
    
    # 将所有结果记录到json中
    for idx,msg in enumerate(slampose):
        json_data = {
            "slampose":{
                "timestamp":slampose[idx][0],
                "position_x":slampose[idx][1].pose.pose.position.x,
                "position_y":slampose[idx][1].pose.pose.position.y,
                "position_z":slampose[idx][1].pose.pose.position.z,
                "orientation_w":slampose[idx][1].pose.pose.orientation.w,
                "orientation_x":slampose[idx][1].pose.pose.orientation.x,
                "orientation_y":slampose[idx][1].pose.pose.orientation.y,
                "orientation_z":slampose[idx][1].pose.pose.orientation.z
            },
            "odom":{
                "timestamp":odom_new[idx][0],
                "position_x":odom_new[idx][1].pose.position.x,
                "position_y":odom_new[idx][1].pose.position.y,
                "orientation_w":odom_new[idx][1].pose.orientation.w,
                "orientation_x":odom_new[idx][1].pose.orientation.x,
                "orientation_y":odom_new[idx][1].pose.orientation.y,
                "orientation_z":odom_new[idx][1].pose.orientation.z
            },
            "whlspd":{
                "timestamp":whlspd_new[idx][0],
                "rear_left":whlspd_new[idx][1].twist.linear.x,
                "rear_right":whlspd_new[idx][1].twist.linear.x
            },
            "imu":{
                "angular_velocity_z":whlspd_new[idx][1].twist.angular.z
            }
        }
        write_json_data(os.path.join(ros_2_jsons_path,str(slampose[idx][0])+'.json'),json_data)

# 3x1的旋转向量转成3x3的旋转矩阵
def toRotationMatrix(rotvector):
    rotmatix = cv2.Rodrigues(rotvector)
    return rotmatix

# 四元数转成欧拉角
def quaternion2euler(quaternion):
    r = R.from_quat(quaternion)
    eular = r.as_euler('xyz',degrees=True)
    return eular

def compute_next_frame_positon(ros_2_jsons_path,pics_path,result_jsons_path):
    if os.listdir(ros_2_jsons_path):
        jsons_list = sorted(os.listdir(ros_2_jsons_path),key=lambda x:x[:-4])
    else:
        print(f"{ros_2_jsons_path}目录下没有json文件！")
    fps_1s = (len(jsons_list)/(int(jsons_list[-1].split('.')[0]) - int(jsons_list[0].split('.')[0])) / (1e-9))
    print(f"帧率:{fps_1s}")
    fps_1s = int(round((len(jsons_list)/(int(jsons_list[-1].split('.')[0]) - int(jsons_list[0].split('.')[0])) / (1e-9)),0))
    
    dist_slam_list,dist_odom_list,agl_deg_slam_list,agl_deg_odom_list = [],[],[],[]
    dist_slam_1s_list,dist_odom_1s_list,agl_deg_slam_1s_list,agl_deg_odom_1s_list = [],[],[],[]
    for i in range(0,len(jsons_list)-1):
        json_data_next_frame = get_json_data(os.path.join(ros_2_jsons_path,jsons_list[i+1]))
        json_data_current_frame = get_json_data(os.path.join(ros_2_jsons_path,jsons_list[i]))
        slampose_curr_px = json_data_current_frame["slampose"]["position_x"]
        slampose_curr_py = json_data_current_frame["slampose"]["position_y"]
        slampose_curr_rw = json_data_current_frame["slampose"]["orientation_w"]
        slampose_curr_rx = json_data_current_frame["slampose"]["orientation_x"]
        slampose_curr_ry = json_data_current_frame["slampose"]["orientation_y"]
        slampose_curr_rz = json_data_current_frame["slampose"]["orientation_z"]
        slampose_next_px = json_data_next_frame["slampose"]["position_x"]
        slampose_next_py = json_data_next_frame["slampose"]["position_y"]
        slampose_next_rw = json_data_next_frame["slampose"]["orientation_w"]
        slampose_next_rx = json_data_next_frame["slampose"]["orientation_x"]
        slampose_next_ry = json_data_next_frame["slampose"]["orientation_y"]
        slampose_next_rz = json_data_next_frame["slampose"]["orientation_z"]
        odom_curr_rw = json_data_current_frame["odom"]["orientation_w"]
        odom_curr_rx = json_data_current_frame["odom"]["orientation_x"]
        odom_curr_ry = json_data_current_frame["odom"]["orientation_y"]
        odom_curr_rz = json_data_current_frame["odom"]["orientation_z"]
        odom_curr_px = json_data_current_frame["odom"]["position_x"]
        odom_curr_py = json_data_current_frame["odom"]["position_y"]
        odom_next_rw = json_data_next_frame["odom"]["orientation_w"]
        odom_next_rx = json_data_next_frame["odom"]["orientation_x"]
        odom_next_ry = json_data_next_frame["odom"]["orientation_y"]
        odom_next_rz = json_data_next_frame["odom"]["orientation_z"]
        odom_next_px = json_data_next_frame["odom"]["position_x"]
        odom_next_py = json_data_next_frame["odom"]["position_y"]

        curr_yaw = quaternion2euler([slampose_curr_rw,slampose_curr_rx,slampose_curr_ry,slampose_curr_rz])[1]        
        next_yaw = quaternion2euler([slampose_next_rw,slampose_next_rx,slampose_next_ry,slampose_next_rz])[1]
        curr_odom_yaw = quaternion2euler([odom_curr_rw,odom_curr_rx,odom_curr_ry,odom_curr_rz])[1]
        next_odom_yaw = quaternion2euler([odom_next_rw,odom_next_rx,odom_next_ry,odom_next_rz])[1]
        spd = (json_data_current_frame["whlspd"]["rear_left"] + json_data_current_frame["whlspd"]["rear_right"]) * 0.5
        agl = json_data_current_frame["imu"]["angular_velocity_z"]
        delta_t = (json_data_next_frame["slampose"]["timestamp"] - json_data_current_frame["slampose"]["timestamp"]) * 1e-9

        calculate_px = spd * delta_t * math.cos(curr_yaw + agl * delta_t * 0.5)
        calculate_py = spd * delta_t * math.sin(curr_yaw + agl * delta_t * 0.5)
        dist_slam = math.sqrt(math.pow((slampose_next_px - (slampose_curr_px +  calculate_px)),2) + math.pow(slampose_next_py - (slampose_curr_py + calculate_py),2))*100
        dist_odom = math.sqrt(math.pow((odom_next_px - (odom_curr_px +  calculate_px)),2) + math.pow(odom_next_py - (odom_curr_py + calculate_py),2))*100
        agl_deg_slam = abs(next_yaw - (curr_yaw + agl * delta_t)) * 180.0 / math.pi
        agl_deg_odom = abs(next_odom_yaw - (curr_odom_yaw + agl * delta_t)) * 180.0 / math.pi
        if agl_deg_slam>90:
            agl_deg_slam = 180 - agl_deg_slam
        if agl_deg_odom>90:
            agl_deg_odom = 180 - agl_deg_odom    
        dist_slam_list.append(dist_slam)
        dist_odom_list.append(dist_odom)
        agl_deg_slam_list.append(agl_deg_slam)
        agl_deg_odom_list.append(agl_deg_odom)
    for i in range(0,len(dist_slam_list)-fps_1s,fps_1s):
        dist_slam_1s,dist_odom_1s,agl_deg_slam_1s,agl_deg_odom_1s = 0,0,0,0
        for j in range(0,fps_1s):
            dist_slam_1s += dist_slam_list[i+j]
            dist_odom_1s += dist_odom_list[i+j]
            agl_deg_slam_1s += agl_deg_slam_list[i+j]
            agl_deg_odom_1s += agl_deg_odom_list[i+j]
        dist_slam_1s_list.append(round(dist_slam_1s/fps_1s,2))
        dist_odom_1s_list.append(round(dist_odom_1s/fps_1s,2))
        agl_deg_slam_1s_list.append(round(agl_deg_slam_1s/fps_1s,2))
        agl_deg_odom_1s_list.append(round(agl_deg_odom_1s/fps_1s,2))
    print(f'''slam最大距离误差:{round(max(dist_slam_list),3)}, odom最大距离误差:{round(max(dist_odom_list),3)}''')
    print(f'''slam最小距离误差:{round(min(dist_slam_list),3)}, odom最小距离误差:{round(min(dist_odom_list),3)}''')
    print(f'''slam平均距离误差:{round(np.mean(dist_slam_list),3)}, odom平均距离误差:{round(np.mean(dist_odom_list),3)}''')
    print(f'''slam距离标准差:{round(np.std(dist_slam_list),3)}, odom距离标准差:{round(np.std(dist_odom_list),3)}''')
    print(f'''slam最大朝向角误差:{round(max(agl_deg_slam_list),3)}, odom最大朝向角误差:{round(max(agl_deg_odom_list),3)}''')
    print(f'''slam最小朝向角误差:{round(min(agl_deg_slam_list),3)}, odom最小朝向角误差:{round(min(agl_deg_odom_list),3)}''')
    print(f'''slam平均朝向角误差:{round(np.mean(agl_deg_slam_list),5)}, odom平均朝向角误差:{round(np.mean(agl_deg_odom_list),5)}''')
    print(f'''slam朝向角标准差:{round(np.std(agl_deg_slam_list),3)}, odom朝向角标准差:{round(np.std(agl_deg_odom_list),3)}''')

    draw_pic_postion(dist_slam_list,dist_odom_list,agl_deg_slam_list,agl_deg_odom_list,pics_path,'Frame(fps)',)
    draw_pic_postion(dist_slam_1s_list,dist_odom_1s_list,agl_deg_slam_1s_list,agl_deg_odom_1s_list,pics_path,'Time(s)')

def compute_1s_avg(result_json_list):
    result_1s_list = []
    first_json = result_json_list[0]
    for i,json_file in enumerate(result_json_list):
        json_name=result_json_list[i].split('.')[0]
        diff = (int(first_json.split('.')[0]) - int(json_file.split('.')[0]))*1e-12
        if diff > 1:
            first_json = json_file
            


def main():
    rosbag_absolute_path = '/home/lixialin/Music/orientation'
    rosbags_path = os.path.join(rosbag_absolute_path,'test_rosbag')
    ros_2_jsons_path = os.path.join(rosbag_absolute_path,'ros_2_jsons')
    pics_path = os.path.join(rosbag_absolute_path,'pic')
    result_jsons_path = os.path.join(rosbag_absolute_path,'result_jsons')
    # 将所有的rosbag都解析成json
    if os.path.exists(ros_2_jsons_path):
        shutil.rmtree(ros_2_jsons_path)
    os.makedirs(ros_2_jsons_path)
    rosbag_list = [x for x in os.listdir(rosbags_path) if x.endswith('.bag')]
    rosbag_list.sort()
    for single_rosbag in rosbag_list:
        rosbag_file = os.path.join(rosbags_path,single_rosbag)        
        analyze_ros_2_json(rosbag_file,ros_2_jsons_path)

    # 根据json中数据，泊车过程slam输出的某一个点，根据规控提供的速度和角度去计算下一个点的位置
    if os.path.exists(result_jsons_path):
        shutil.rmtree(result_jsons_path)
    os.makedirs(result_jsons_path)
    if os.path.exists(pics_path):
        shutil.rmtree(pics_path)
    os.makedirs(pics_path)
    compute_next_frame_positon(ros_2_jsons_path,pics_path,result_jsons_path)


    

if __name__=='__main__':
    main()