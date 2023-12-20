import os
import shutil
import pathlib
import rosbag,rospy
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import utils
import config


def signal_ros_2_json(rosbag_file,json_path,timestamp_file):
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
    with open(timestamp_file,'r') as f:
        for lines in f.readlines():
            timestamp_ = int(lines.strip().split(' ')[-1])
            timestamp_2_frameid[timestamp_] = int(lines.split(' ')[1])
    
    # 根据NM时间戳，获取视频对应帧id。将EQ和NM想要的数据，存放到json中
    for i in range(len(nm_list)):
        timestamp_ = int(nm_list[i].header.stamp.secs*1000000 + nm_list[i].header.stamp.nsecs/1000)
        json_path_file =  os.path.join(json_path, str(timestamp_2_frameid[timestamp_])+ '.json')
        eq_cipv_id = eq_new_list[i].cipv_id
        eq_px,eq_py = -1,-1
        eq_data,nm_data = {},{}
        nm_data_list = []        
        for obs in eq_new_list[i].tracks:    
            obs_id = obs.id
            if int(eq_cipv_id)==int(obs_id): 
                eq_type_value = int(obs.type)
                if eq_type_value >4:
                    continue
                eq_type = config.eq4_config["obs_type"][eq_type_value]
                # 障碍物长宽，eq不输出高度，ros中写死的1.5m;ros中x对应h,y对应w,z对应l
                eq_w = obs.bbox3d.size.y
                eq_l = obs.bbox3d.size.z
                # 横纵向距离，EQ4的相机输出的结果是基于“前轴中心”到“车尾”的距离，蒙4轴距：2736.01mm，T22车辆轴距：2815mm
                wheelbase = 2.815
                eq_px = obs.position.x + wheelbase + eq_l/2
                eq_py = -(obs.position.y + 0.215)
                # 横纵向速度，相对速度
                eq_vx = obs.velocity.x
                eq_vy = obs.velocity.y
                # 障碍物航向角,看代码没有接入航向角：OBJ_Angle_Mid_i（需要跟研发确认）
                # yaw = obs.rotation.yaw
                eq_data = {
                    "type":eq_type,
                    "px":eq_px,
                    "py":eq_py,
                    "vx":eq_vx,
                    "vy":eq_vy,
                    "w":eq_w,
                    "l":eq_l
                }
        if eq_px==-1:
            continue
        uv_px,uv_py = world_2_uv(eq_px,eq_py)
        scale = 2.4
        top_cut = 200
        uv_px = int(uv_px/scale)
        uv_py = int((uv_py-top_cut)/scale) 
        for obs in nm_list[i].tracks:
            # 2D上的障碍物的左上角点和宽高
            if int(obs.type)==0:
                continue
            nm_type = config.front_config["enum_obstacle3"][obs.type]
            nm_2d_x = obs.uv_bbox2d.left_top.x
            nm_2d_y = obs.uv_bbox2d.left_top.y
            nm_2d_w = obs.uv_bbox2d.size.x
            nm_2d_h = obs.uv_bbox2d.size.y
            if nm_2d_x<= uv_px <= (nm_2d_x+nm_2d_w) and nm_2d_y<= uv_py <=(nm_2d_y+nm_2d_h):
                nm_px = obs.position.x
                nm_py = obs.position.y
                nm_vx = obs.velocity.x
                nm_vy = obs.velocity.y
                nm_w = obs.bbox3d.size.y
                nm_l = obs.bbox3d.size.z
                nm_data_ = {
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
                nm_data_list.append(nm_data_)
        if len(nm_data_list) ==  0:
            continue
        elif len(nm_data_list) == 1:
            nm_data = nm_data_list[0]
        else:
            nm_px_list = [x["px"] for x in nm_data_list ]
            idx = nm_px_list.index((min(nm_px_list)))
            nm_data = nm_data_list[idx]
        json_data = {
            "nm_timestamp":nm_time_list[i],
            "eq_timestamp":eq_new_time_list[i],
            "eq_cipv_id":eq_cipv_id,
            "eq_data":eq_data,
            "nm_data":nm_data
        }
        utils.write_json_data(json_path_file,json_data)

def world_2_uv(eq_px,eq_py):       
    eq_z = 0.7
    world_p = np.array([eq_px,eq_py,eq_z,1])
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
    return x1/z1,y1/z1

def same_cipv_in_one_dir(json_path,same_cipv_dir):
    num = 1
    first_cipv_id = -1
    target_path = -1
    for root,dirs,files in os.walk(json_path):
        files.sort()
        new_files = sorted(files,key=lambda x:int(x[:-5]))      
        for i in range(len(new_files)):
            json_data = utils.get_json_data(os.path.join(root,new_files[i]))
            last_cipv_id = json_data["eq_cipv_id"]
            if last_cipv_id!=first_cipv_id:
                target_path = os.path.join(same_cipv_dir,str(num))
                os.makedirs(target_path,exist_ok=True)
                num +=1
                os.system('cp {} {}'.format(os.path.join(root,new_files[i]),target_path))
                first_cipv_id = last_cipv_id
            else:
                first_cipv_id = last_cipv_id
                os.system('cp {} {}'.format(os.path.join(root,new_files[i]),target_path))

def clean_data(json_data,new_same_cipv_dir,continue_cipv_num):
    num = 1
    for root,dirs,files in os.walk(json_data):
        for dir_ in dirs:
            json_files = [x for x in os.listdir(os.path.join(root,dir_)) if x.endswith('.json')]
            if len([x for x in os.listdir(os.path.join(root,dir_)) if x.endswith('.json')]) <continue_cipv_num:
                os.system('rm -r {}'.format(os.path.join(root,dir_)))
            new_json_files = sorted(json_files,key=lambda x:int(x[:-5]))
            sum = 0
            for i in range(len(new_json_files)-1):
                if (int(new_json_files[i+1][:-5])-int(new_json_files[i][:-5]))==1:
                    sum +=1
                else:
                    if sum < continue_cipv_num:
                        sum =0
                        continue
                    else: 
                        new_json_dir = os.path.join(new_same_cipv_dir,str(num))
                        os.makedirs(new_json_dir)
                        print(f"{new_json_dir}目录下，连续cipv的json数量：{sum}")
                        num +=1
                        for j in range(0,i):    
                            os.system('cp {} {}'.format(os.path.join(root,dir_,new_json_files[j]),new_json_dir))
            
def rosbag_2_json(rosbag_dir_path,timestamp_file,json_path):
    rosbag_list = [x for x in os.listdir(rosbag_dir_path) if x.endswith('.bag')]
    for rosbag_ in rosbag_list:
        rosbag_file = os.path.join(rosbag_dir_path,rosbag_)
        signal_ros_2_json(rosbag_file,json_path,timestamp_file)

def draw_distance_time_seq_pic(eq_value,nm_value,dst_path,title,value_range,ylabel):           
    plt.figure(figsize=(18,10))
    plt.ylim(value_range)
    plt.title(title)
    plt.plot(eq_value,label=('eq_' + ylabel.lower()))
    plt.plot(nm_value,label=('nm_' + ylabel.lower()))
    plt.legend(loc='lower right')
    plt.xlabel('FrameID')
    plt.ylabel(ylabel)
    # plt.show()
    plt.savefig(os.path.join(dst_path,title +'.png'))

# def draw_distance_speed_pic(eq_distance,nm_distance,eq_speed,nm_speed,dst_path,title,value_range):
#     plt.figure(figsize=(18,10))
#     plt.ylim(value_range)
#     plt.title(title)
#     plt.plot(eq_distance,eq_speed,label='eq_speed')
#     plt.plot(nm_distance,nm_speed,label='nm_speed')
#     plt.legend(loc='lower right')
#     plt.xlabel('Distance')
#     plt.ylabel('Speed')
#     # plt.show()
#     plt.savefig(os.path.join(dst_path,title +'.png'))


def draw_pic(new_same_cipv_dir,pic_dst_path):
    for root,dirs,files in os.walk(new_same_cipv_dir):
        for dir_ in dirs:
            print(dir_)
            json_files = [x for x in os.listdir(os.path.join(root,dir_)) if x.endswith('.json')]
            new_json_files = sorted(json_files,key=lambda x:int(x[:-5]))
            eq_h_distance,eq_z_distance,eq_h_speed,eq_z_speed = [],[],[],[]
            nm_h_distance,nm_z_distance,nm_h_speed,nm_z_speed = [],[],[],[]
            for json_ in new_json_files:
                json_data = utils.get_json_data(os.path.join(root,dir_,json_))
                eq_z_distance.append(json_data["eq_data"]["px"])
                eq_h_distance.append(json_data["eq_data"]["py"])
                eq_z_speed.append(json_data["eq_data"]["vx"])
                eq_h_speed.append(json_data["eq_data"]["vy"])
                nm_z_distance.append(json_data["nm_data"]["px"])
                nm_h_distance.append(json_data["nm_data"]["py"])
                nm_z_speed.append(json_data["nm_data"]["vx"])
                nm_h_speed.append(json_data["nm_data"]["vy"])
            dst_path = os.path.join(pic_dst_path,dir_)
            os.makedirs(dst_path)
            draw_distance_time_seq_pic(eq_h_distance,nm_h_distance,dst_path,'LateralDistance',(-5,5),'Distance')
            draw_distance_time_seq_pic(eq_z_distance,nm_z_distance,dst_path,'LongitudinalDistance',(0,100),'Distance')
            draw_distance_time_seq_pic(eq_h_speed,nm_h_speed,dst_path,'LateralSpeed',(0,20),'Speed')
            draw_distance_time_seq_pic(eq_z_speed,nm_z_speed,dst_path,'LongitudinalSpeed',(0,100),'Speed')
            # draw_distance_speed_pic(eq_h_distance,nm_h_distance,eq_h_speed,nm_h_speed,dst_path,'LateralDistance-Speed',(0,30))
            # draw_distance_speed_pic(eq_z_distance,nm_z_distance,eq_z_speed,nm_z_speed,dst_path,'LongitudinalDistance-Speed',(0,120))
                       

def main():
    rosbag_dir_path = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d1/0_temp/2023-10-07_2'
    timestamp_file = os.path.join(rosbag_dir_path,'video_record','2023-2-27_10-38-58','timestamp.log')
    pic_dst_path = os.path.join(rosbag_dir_path,'draw_pic')
    json_path = os.path.join(rosbag_dir_path,'json_cipv')   
    same_cipv_dir = os.path.join(rosbag_dir_path,'same_json_cipv')
    new_same_cipv_dir = os.path.join(rosbag_dir_path,'new_same_json_cipv')
    continue_cipv_num =100
    # 将eyeq4的cipv取出，并投影到NM图片上，且判断eyeq的点在nm的2d框内，则生成json
    # if os.path.exists(json_path):
    #     shutil.rmtree(json_path)
    # os.makedirs(json_path)
    # rosbag_2_json(rosbag_dir_path,timestamp_file,json_path)

    # 遍历所有的cipv的json，把cipv相同的放到一个文件夹中
    # if os.path.exists(same_cipv_dir):
    #     shutil.rmtree(same_cipv_dir)
    # os.makedirs(same_cipv_dir)
    # same_cipv_in_one_dir(json_path,same_cipv_dir)

    # 数据清洗，删除连续数据小于100张的数据
    # if os.path.exists(new_same_cipv_dir):
    #     shutil.rmtree(new_same_cipv_dir)
    # os.makedirs(new_same_cipv_dir)
    # clean_data(same_cipv_dir,new_same_cipv_dir,continue_cipv_num)

    # 处理json数据，画EQ和NM的对比图。横纵向距离时序图、横纵向距离-相对速度曲线图
    if os.path.exists(pic_dst_path):
        shutil.rmtree(pic_dst_path)
    os.makedirs(pic_dst_path)
    draw_pic(new_same_cipv_dir,pic_dst_path)

if __name__=='__main__':
    main()