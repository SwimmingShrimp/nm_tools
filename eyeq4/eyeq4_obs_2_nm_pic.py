import os
import rosbag
import numpy as np
import math
import cv2
import rospy
import sys
sys.path.append('..')
import utils
import config
import shutil


def analyze_ros_2_json(rosbag_file,json_path):
    bag_data = rosbag.Bag(rosbag_file,'r')
    nm_list,eq_list,nm_time_list,eq_time_list = [],[],[],[]
    '''
    rosbag中，for topic,msg,t中的t是rosbag文件记录的时间，取的是记录文件的设备的系统时间
    msg中的header.stamp下的时间，是消息发出的时间
    '''
    for topic,msg,t in bag_data.read_messages("/perception/obstacle_list"):
        nm_list.append(msg)
        nm_time_list.append(rospy.Time.to_nsec(t))
    for topic,msg,t in bag_data.read_messages("/perception/eq4_obstacle_list"):
        eq_list.append(msg)
        eq_time_list.append(rospy.Time.to_nsec(t))

    # for topic,msg,t in bag_data.read_messages("/perception/obstacle_list"):
    #     nm_list.append(msg)
    #     nm_time_list.append(int(msg.header.stamp.secs*1000000 + msg.header.stamp.nsecs/1000))
    # for topic,msg,t in bag_data.read_messages("/perception/eq4_obstacle_list"):
    #     eq_list.append(msg)
    #     eq_time_list.append(int(msg.header.stamp.secs*1000000 + msg.header.stamp.nsecs/1000))
    
    # 根据NM的时间取最近时间戳，来对齐NM和EQ的数据帧
    eq_new_time_list,eq_new_list = [],[]
    for i in range(len(nm_time_list)):
        diff = abs(nm_time_list[i] - eq_time_list[i])
        nm_2_eq = i
        for j in range(len(eq_time_list)):
            diff_new = abs(nm_time_list[i] - eq_time_list[j])
            if diff_new < diff:
                nm_2_eq = j
                diff = diff_new
        eq_new_time_list.append(eq_time_list[nm_2_eq])
        eq_new_list.append(eq_list[nm_2_eq])

    # 根据rosbag中的时间戳文件，获取到图片帧数的字典
    timestamp_2_frameid = {}
    with open('/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/0_temp/2023-10-07_2/video_record/2023-2-27_10-38-58/timestamp.log','r') as f:
        for lines in f.readlines():
            timestamp_ = int(lines.strip().split(' ')[-1])
            timestamp_2_frameid[timestamp_] = int(lines.split(' ')[1])
    
    # 根据NM时间戳，获取视频对应帧id。将EQ和NM想要的数据，存放到json中
    for i in range(len(nm_list)):
        timestamp_ = int(nm_list[i].header.stamp.secs*1000000 + nm_list[i].header.stamp.nsecs/1000)
        json_path_file =  os.path.join(json_path, str(timestamp_2_frameid[timestamp_])+ '.json')
        json_data = {
            "nm_timestamp":nm_time_list[i],
            "eq_timestamp":eq_new_time_list[i],
            "nm":[],
            "eq":[]
        }

        for obs in nm_list[i].tracks:
            # 2D上的障碍物的左上角点和宽高
            if int(obs.type)==0:
                continue
            nm_type = config.front_config["enum_obstacle3"][obs.type]
            nm_2d_x = obs.uv_bbox2d.left_top.x
            nm_2d_y = obs.uv_bbox2d.left_top.y
            nm_2d_w = obs.uv_bbox2d.size.x
            nm_2d_h = obs.uv_bbox2d.size.y
            nm_px = obs.position.x
            nm_py = obs.position.y
            nm_vx = obs.velocity.x
            nm_vy = obs.velocity.y
            nm_w = obs.bbox3d.size.y
            nm_l = obs.bbox3d.size.z
            nm_data = {
                'type':nm_type,
                '2d_x':nm_2d_x,
                '2d_y':nm_2d_y,
                '2d_w':nm_2d_w,
                '2d_h':nm_2d_h,
                "px":nm_px,
                "py":nm_py,
                "vx":nm_vx,
                "vy":nm_vy,
                "w":nm_w,
                "l":nm_l
            }
            json_data["nm"].append(nm_data)

        for obs in eq_new_list[i].tracks:
            eq_type_value = int(obs.type)
            if eq_type_value >4:
                continue
            eq_type = config.eq4_config["obs_type"][eq_type_value]
            # 障碍物长宽，eq不输出高度，ros中写死的1.5m;ros中x对应h,y对应w,z对应l
            w = obs.bbox3d.size.y
            l = obs.bbox3d.size.z
            # 横纵向距离，EQ4的相机输出的结果是基于“前轴中心”到“车尾”的距离，蒙4轴距：2736.01mm，T22车辆轴距：2815mm
            wheelbase = 2.815
            px = obs.position.x + wheelbase + l/2
            py = -(obs.position.y + 0.215)
            # 横纵向速度，相对速度
            vx = obs.velocity.x
            vy = obs.velocity.y
            # 障碍物航向角,看代码没有接入航向角：OBJ_Angle_Mid_i（需要跟研发确认）
            # yaw = obs.rotation.yaw
            eq_data = {
                "type":eq_type,
                "px":px,
                "py":py,
                "vx":vx,
                "vy":vy,
                "w":w,
                "l":l
            }
            json_data["eq"].append(eq_data)
        utils.write_json_data(json_path_file,json_data)

def world_2_uv(world_point):    
    x = world_point[0] 
    y = world_point[1]
    z = 0.7
    world_p = np.array([x,y,z,1])
    # 相机外参:相机到车体，4x4旋转平移矩阵
    R = np.array([[-0.  ,-0.0008239203419564778,0.9999935694272383,2.09],
         [-0.9998964322674533,0.013965136104336242,-0.0034784640871957694,0],
         [-0.013962180323192191,-0.9999021432764598,-0.0008725776556789232,1.41],
         [0,0,0,1]])
    # 相机内参
    camera_in_params = np.array([[1010.2361246437642,0,971.524849288821,0],
                                 [0,1009.9933610930672,542.6131924168506,0],
                                 [0,0,1,0]])
    # 世界坐标系--转成-->像素坐标系
    uv_point = np.matmul(camera_in_params,np.matmul((np.linalg.inv(R)),world_p))
    x1,y1,z1 = uv_point.tolist()
    # if x1<0 or y1<0:
    #     return -1,-1
    return x1/z1,y1/z1
    
def draw_eq_circle_nm_rectangle(img_src,file_data,file_,new_img_path): 
    print(os.path.join(new_img_path,str(int(file_[:-5]))+'.png'))
    img = cv2.imread(os.path.join(img_src,str(int(file_[:-5]))+'.png'))
    scale = 2.4
    top_cut = 200
    for file_data_ in file_data["eq"]:
        px = file_data_["px"]
        py = file_data_["py"]                   
        ux,uy = world_2_uv((px,py))
        if ux==-1 or uy==-1:
            continue
        ux = int(ux/scale)
        uy = int((uy-top_cut)/scale)
        cv2.circle(img,(ux,uy+256),3,(255,0,255),-1)
        cv2.putText(img,file_data_["type"],(ux,uy+256-10),cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,0,255),1)
    for file_data_ in file_data["nm"]:
        x = int(file_data_["2d_x"])
        y = int(file_data_["2d_y"]) +256
        w = int(file_data_["2d_w"])
        h = int(file_data_["2d_h"])
        cv2.rectangle(img,(x,y),((x+w),(y+h)),(0,255,0),1)
        cv2.putText(img,file_data_["type"],((x,y+10)),cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,255,0),1)
    cv2.imwrite(os.path.join(new_img_path,file_[:-4]+'png'),img)


def main():
    rosbag_src = "/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/0_temp/2023-10-07_2"
    img_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/0_temp/2023-10-07_2/video_record/2023-2-27_10-38-58/pic'
    new_img_path = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/0_temp/2023-10-07_2/new_pic'
    os.makedirs(new_img_path,exist_ok=True)
    # 将rosbag解析成json
    # rosbag_list = [x for x in os.listdir(rosbag_src) if x.endswith('.bag')]
    # rosbag_list.sort()
    # for single_rosbag in rosbag_list:
    #     rosbag_file = os.path.join(rosbag_src,single_rosbag)
    #     json_path = os.path.join(rosbag_src,'json',single_rosbag[:-4])
    #     shutil.rmtree(json_path)
    #     os.makedirs(json_path,exist_ok=True)
    #     analyze_ros_2_json(rosbag_file,json_path)
    # 将感知结果和eq结果画到图片上
    for root,dirs,files in os.walk(os.path.join(rosbag_src,'json')):
        files.sort()
        for file_ in files:
            file_data = utils.get_json_data(os.path.join(root,file_))
            draw_eq_circle_nm_rectangle(img_src,file_data,file_,new_img_path)

if __name__=='__main__':
    main()