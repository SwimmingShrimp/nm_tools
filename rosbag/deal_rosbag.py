from runpy import _TempModule
import rosbag
import utils
import os
import shutil
import config
import random
import numpy as np

# 将感知结果的rosbag包处理成评测需要的json文件格式
def get_msg_tracks(msg):
    json_data_list =[]
    if msg.tracks!=[]:
        for temp in msg.tracks:
            camera_id = temp.camera_position
            obsatcle_type = temp.type
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
                "type":obsatcle_type,
                "box_2d":box_2d,
                "box_3d":box_3d,
                "distance":distance,
                # "yaw":yaw,
                "camera_id":camera_id
            }
            json_data_list.append(json_content)
    return json_data_list

def get_detect_util(msg):
    json_data_list =[]
    seq = msg.header.seq
    if msg.single_obstacles!=[]:
        for temp in msg.single_obstacles:
            obstacle_type = temp.type
            box2d = {
                "x":temp.uv_bbox2d.left_top.x,
                "y":temp.uv_bbox2d.left_top.y,
                "w":temp.uv_bbox2d.size.x,
                "h":temp.uv_bbox2d.size.y
            }
            perce_dist = temp.depth
            json_content = {
                "obstacle_type":obstacle_type,
                "box2d":box2d,
                "perce_dist":perce_dist
            }
            json_data_list.append(json_content)
    return seq,json_data_list

def get_tl_detect_util(msg):
    json_data_list =[]
    seq = msg.header.seq
    if msg.single_traffic_lights!=[]:
        for temp in msg.single_traffic_lights:
            box2d = {
                "x":temp.uv_bbox2d.left_top.x,
                "y":temp.uv_bbox2d.left_top.y,
                "w":temp.uv_bbox2d.size.x,
                "h":temp.uv_bbox2d.size.y
            }
            tl_shape_type = temp.tl_shape_type
            tl_forward_type = temp.tl_forward_type
            tl_left_type = temp.tl_left_type
            tl_right_type = temp.tl_right_type
            tl_uturn_type = temp.tl_uturn_type
            # tl_detection = str(tl_forward_type) + '_' +str(tl_left_type) + '_'+ str(tl_right_type) + '_' +str(tl_uturn_type)
            tl_detection = [int(tl_forward_type),int(tl_left_type),int(tl_right_type),int(tl_uturn_type)]
            print("bag:",tl_detection)
            json_content = {
                "tl_shape_type":tl_shape_type,
                "tl_detection":tl_detection,
                "box2d":box2d,
            }
            json_data_list.append(json_content)
    return seq,json_data_list

def get_tsr_detect_util(msg):
    json_data_list =[]
    seq = msg.header.seq
    if msg.single_traffic_signs!=[]:
        for temp in msg.single_traffic_signs:
            obstacle_type = config.front_tsr["enum_obstacle"][temp.ts_subclass_index]
            is_min = temp.ts_attrs_score_min
            is_end = temp.ts_attrs_score_end
            is_led = temp.ts_attrs_score_led
            is_ring = temp.ts_attrs_score_ring
            
            box2d = {
                "x":temp.uv_bbox2d.left_top.x,
                "y":temp.uv_bbox2d.left_top.y,
                "w":temp.uv_bbox2d.size.x,
                "h":temp.uv_bbox2d.size.y
            }
            #perce_dist = temp.depth
            perce_dist = random.randint(3,100) 
            json_content = {
                "obstacle_type":obstacle_type,
                "is_min":is_min,
                "is_end":is_end,
                "is_led":is_led,
                "is_ring":is_ring,
                "box2d":box2d,                
                "perce_dist":perce_dist
            }
            json_data_list.append(json_content)
    return seq,json_data_list

def get_tl_msg_tracks(msg):
    json_data_list =[]
    if msg.traffic_light_groups[0].traffic_light_msgs!=[]:
        for temp in msg.traffic_light_groups[0].traffic_light_msgs:
            forward_status = temp.forward_state.valid_state
            left_status = temp.left_state.valid_state
            right_status = temp.right_state.valid_state
            uturn_status = temp.uturn_state.valid_state
            light_status = str(forward_status) + '_' + str(left_status) + '_' + str(right_status) + '_' + str(uturn_status)
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
                "light_status":light_status,
                "forward_status":forward_status,
                "left_status":left_status,
                "right_status":right_status,
                "uturn_status":uturn_status
            }
            json_data_list.append(json_content)
    return json_data_list

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

def get_lane_3d_info(lane_msg, veh2uv_msg):
    json_data_dict ={}
    lanes_info = lane_msg[1].lanes
    veh2uv_info = veh2uv_msg[1].veh2uv_mats
    
    json_data_dict['task_lane'] = []
    json_data_dict['task_roadedge'] = []
    json_data_dict["veh2uv_mats"] = {}
    # parse lane info
    if lanes_info!=[]:
        
        for temp in lanes_info:
            position = int(temp.position)
            if 0< int(position) <7: # 所有实例车道线
                curve_parameter = {
                    "c0":temp.position_parameter_c0,
                    "c1":temp.heading_angle_parameter_c1,
                    "c2":temp.curvature_parameter_c2,
                    "c3":temp.curvature_derivative_parameter_c3
                }
                noparking =temp.no_parking
                woven_lane_type = temp.guide_lane.type
                stop_lane_type = temp.stop_lane.type
                arrow_type = temp.grd_sign.type
                
                # 此时该车道线若存在地面标识，就赋予正确的box
                if woven_lane_type == 6:
                    box = [[n.x/100, n.y/100, n.z/100] for n in temp.guide_lane.box]
                    center = temp.guide_lane.center
                    woven_lane = dict(
                        type = woven_lane_type,
                        box = box,
                        center = [center.x/100, center.y/100, center.z/100]
                    )
                    
                else:
                    woven_lane = dict()
                    
                if stop_lane_type == 9:
                    box = [[n.x, n.y, n.z] for n in temp.stop_lane.box]
                    center = temp.stop_lane.center
                    stoplane = dict(
                        type = stop_lane_type,
                        box = box,
                        center = [center.x, center.y, center.z]
                    )
                    
                else:
                    stoplane = dict()
                    
                if 16<=arrow_type <=26:
                    box = [[n.x/100, n.y/100, n.z/100] for n in temp.grd_sign.box]
                    center = temp.grd_sign.center
                    arrow = dict(
                        type = arrow_type, 
                        box = box,
                        center = [center.x/100, center.y/100, center.z/100]
                        )
                else:
                    arrow = dict()
                    
                type = temp.type
                color = temp.color
                start = temp.view_range_start
                end = temp.view_range_end
                
                
                lane_content = dict(
                    position=position,
                    type = type,
                    color = color,
                    start = start,
                    end = end,
                    curve_parameter = curve_parameter,
                    no_parking = noparking,
                    woven_lane = woven_lane,
                    stop_lane = stoplane,
                    arrow = arrow,
                )
                json_data_dict['task_lane'].append(lane_content)
                
            # 如果输出位置是路沿
            elif 7 <= position <=8:
                curve_parameter = {
                    "c0":temp.position_parameter_c0,
                    "c1":temp.heading_angle_parameter_c1,
                    "c2":temp.curvature_parameter_c2,
                    "c3":temp.curvature_derivative_parameter_c3
                }
                type = temp.type
                start = temp.view_range_start
                end = temp.view_range_end
                roadedge_content = dict(
                    position=position,
                    type = type,
                    start = start,
                    end = end,
                    curve_parameter = curve_parameter,
                )
                json_data_dict['task_roadedge'].append(roadedge_content)
                
    json_data_dict['task_lane'] = sorted(json_data_dict['task_lane'], key=lambda x: int(x["position"]))
    json_data_dict['task_roadedge'] = sorted(json_data_dict['task_roadedge'], key=lambda x: int(x["position"]))
    
    if len(veh2uv_info) != 0:
        front_far_mat = np.array(veh2uv_info[1].veh2uv_mat).reshape((4, 3)).transpose()
        front_near_mat = np.array(veh2uv_info[2].veh2uv_mat).reshape((4, 3)).transpose()
        json_data_dict["veh2uv_mats"]["front_far"] = front_far_mat.tolist()
        json_data_dict["veh2uv_mats"]["front_near"] = front_near_mat.tolist()
        
    return json_data_dict

def get_freespace_info(freespace_msg, veh2uv_msg):
    json_data_dict ={}
    freespace_info = freespace_msg[1].edge
    veh2uv_info = veh2uv_msg[1].veh2uv_mats

    json_data_dict['task_freespace'] = []
    json_data_dict["veh2uv_mats"] = {}
    # parse lane info

    if len(freespace_info) != 0:
        
        # 单位是厘米,转换成米
        point = [[n.x/100, n.y/100, n.z/100] for n in freespace_info]
        freespace_content = dict(
            point = point
        )
        json_data_dict['task_freespace'].append(freespace_content)
    
    if len(veh2uv_info) != 0:
        
        front_far_mat = np.array(veh2uv_info[1].veh2uv_mat).reshape((4, 3)).transpose()
        front_near_mat = np.array(veh2uv_info[2].veh2uv_mat).reshape((4, 3)).transpose()
        json_data_dict["veh2uv_mats"]["front_far"] = front_far_mat.tolist()
        json_data_dict["veh2uv_mats"]["front_near"] = front_near_mat.tolist()
        
    return json_data_dict

def get_detct_bag(bag_file,dst,eval_type):
    bag_data = rosbag.Bag(bag_file,'r')
    if eval_type=='front_rp':
        for temp in ['/perception/front_far_obstacle','/perception/front_near_obstacle']:
            dirname = temp.split('/')[-1].rsplit('_',1)[0]
            obstacle_data = bag_data.read_messages(temp)
            for topic,msg, t in obstacle_data:    
                frame_id,json_data = get_detect_util(msg)
                json_name = str(frame_id) + '.json'
                os.makedirs(os.path.join(dst,dirname),exist_ok=True)
                utils.write_json_data(os.path.join(dst,dirname,json_name),json_data)
    elif eval_type=='side_rp':
        for temp in ['/perception/side_left_front_obstacle','/perception/side_left_rear_obstacle','/perception/side_right_front_obstacle','/perception/side_right_rear_obstacle']:
            dirname = temp.split('/')[-1].rsplit('_',1)[0]
            obstacle_data = bag_data.read_messages(temp)
            for topic,msg, t in obstacle_data:
                frame_id, json_data = get_detect_util(msg)
                json_name = str(frame_id) + '.json'
                os.makedirs(os.path.join(dst,dirname),exist_ok=True)
                utils.write_json_data(os.path.join(dst,dirname,json_name),json_data)
    elif eval_type=='back_rp':
        for temp in ['/perception/back_middle_obstacle']:
            dirname = temp.split('/')[-1].rsplit('_',1)[0]
            obstacle_data = bag_data.read_messages(temp)
            for topic,msg, t in obstacle_data:
                frame_id,json_data = get_detect_util(msg)
                json_name = str(frame_id) + '.json'
                os.makedirs(os.path.join(dst,dirname),exist_ok=True)
                utils.write_json_data(os.path.join(dst,dirname,json_name),json_data)
    elif eval_type=='tl_rp':
        for temp in ['/perception/front_far_obstacle','/perception/front_near_obstacle']:
            dirname = temp.split('/')[-1].rsplit('_',1)[0]
            obstacle_data = bag_data.read_messages(temp)
            for topic,msg, t in obstacle_data:
                frame_id,json_data = get_tl_detect_util(msg)
                json_name = str(frame_id) + '.json'
                os.makedirs(os.path.join(dst,dirname),exist_ok=True)
                utils.write_json_data(os.path.join(dst,dirname,json_name),json_data)
    elif eval_type=='tsr_rp':
        for temp in ['/perception/front_far_obstacle','/perception/front_near_obstacle']:
            dirname = temp.split('/')[-1].rsplit('_',1)[0]
            obstacle_data = bag_data.read_messages(temp)
            for topic,msg, t in obstacle_data:
                frame_id,json_data = get_tsr_detect_util(msg)
                json_name = str(frame_id) + '.json'
                os.makedirs(os.path.join(dst,dirname),exist_ok=True)
                utils.write_json_data(os.path.join(dst,dirname,json_name),json_data)

def get_bag_data(bag_file,dst,num,eval_type):
    bag_data = rosbag.Bag(bag_file,'r')
    if eval_type=='tl_dist':
        obstacle_data = bag_data.read_messages('/perception/traffic_lights')
        frame_id = num
        for topic,msg, t in obstacle_data:
            json_name = str(frame_id) + '.json'
            frame_id +=1
            json_data = get_tl_msg_tracks(msg)
            utils.write_json_data(os.path.join(dst,json_name),json_data)
    elif eval_type=='tsr_dist':
        obstacle_data = bag_data.read_messages('/perception/traffic_signs')
        frame_id = num
        for topic,msg, t in obstacle_data:
            json_name = str(frame_id) + '.json'
            frame_id +=1
            json_data = get_tsr_msg_tracks(msg)
            utils.write_json_data(os.path.join(dst,json_name),json_data)    
    elif eval_type=='front_dist':
        obstacle_data = bag_data.read_messages('/perception/obstacle_list')
        frame_id = num
        for topic,msg, t in obstacle_data:
            json_name = str(frame_id) + '.json'
            frame_id +=1
            json_data = get_msg_tracks(msg)
            utils.write_json_data(os.path.join(dst,json_name),json_data)       
    elif eval_type == 'lane_3d':
        lane_data = bag_data.read_messages('/perception/L0lka_lane_list/')
        veh2uv_data = bag_data.read_messages('/perception/veh2uv_matrixs/')
        frame_id = num
        for lane_msg, veh2uv_msg in zip(lane_data, veh2uv_data):
            json_name = str(frame_id) + '.json'
            frame_id += 1
            json_data = get_lane_3d_info(lane_msg, veh2uv_msg)
            utils.write_json_data(os.path.join(dst,json_name),json_data)
                      
    elif eval_type == 'freespace':
        freespace_data = bag_data.read_messages('/perception/freespace_contour/')
        veh2uv_data = bag_data.read_messages('/perception/veh2uv_matrixs/')
        for freespace_msg, veh2uv_msg in zip(freespace_data, veh2uv_data):
            frame_id = freespace_msg[1].header.seq
            json_name = str(frame_id) + '.json'
            json_data = get_freespace_info(freespace_msg, veh2uv_msg)
            utils.write_json_data(os.path.join(dst,json_name),json_data)

def get_fusion_bag(fusion_bag,dst):
    bag_data = rosbag.Bag(fusion_bag,'r')
    topic_list = ["/perception/obstacle_list","/fusion/obstacle_list"]
    bag_data = bag_data.read_messages(topic_list)
    bag_data_list = [[msg_type, msg, time_stamp] for msg_type, msg, time_stamp in bag_data]
    temp_cam_frame_list = []
    for bag_data in bag_data_list:
        if (bag_data[0] == "/perception/obstacle_list"):
            # 用于保存10帧的视觉pb消息
            temp_cam_frame_list.append(bag_data[1])
            if len(temp_cam_frame_list) > 10:
                temp_cam_frame_list.pop(0)
        # 找到一帧融合
        if (bag_data[0] == "/fusion/obstacle_list"):
            json_data_list =[]
            # 对于该帧融合中所有的障碍物
            for fused_obstacle in bag_data[1].tracks:
                # 取出视觉的id
                match_camera_obs_id = fused_obstacle.associate_infos[0].id
                # 取出该融合对应的视觉的时间戳
                ass_camera_time_stamp_secs = fused_obstacle.associate_infos[0].stamp.secs
                ass_camera_time_stamp_nsecs = fused_obstacle.associate_infos[0].stamp.nsecs
                # 从上面保存的视觉的list中找到对应的帧
                for cam_obs_frame in temp_cam_frame_list:
                    if cam_obs_frame.send_time.secs == ass_camera_time_stamp_secs and \
                        cam_obs_frame.send_time.nsecs  == ass_camera_time_stamp_nsecs:
                        seq = cam_obs_frame.header.seq
                        # 找到对应的视觉障碍物
                        for cam_track in cam_obs_frame.tracks:
                            if match_camera_obs_id == cam_track.id:
                                distance = {
                                "x":fused_obstacle.position.x,
                                "y":fused_obstacle.position.y
                                }
                                camera_id = cam_track.camera_position
                                type = cam_track.type
                                box_2d = {
                                    "x":cam_track.uv_bbox2d.left_top.x,
                                    "y":cam_track.uv_bbox2d.left_top.y,
                                    "w":cam_track.uv_bbox2d.size.x,
                                    "h":cam_track.uv_bbox2d.size.y
                                }
                                box_3d = {
                                    "l":cam_track.bbox3d.size.x,
                                    "w":cam_track.bbox3d.size.y,
                                    "h":cam_track.bbox3d.size.z
                                }
                                yaw = cam_track.rotation.yaw
                                json_content = {
                                    "type":type,
                                    "box_2d":box_2d,
                                    "box_3d":box_3d,
                                    "distance":distance,
                                    "yaw":yaw,
                                    "camera_id":camera_id
                                }
                                json_data_list.append(json_content)
                                utils.write_json_data(os.path.join(dst,(str(seq)+'.json')),json_data_list)
                    else:
                        continue    
        


def find_rosbag_path(rosbag_dir):
    bag_list = []
    for (roots, dirs, files) in os.walk(rosbag_dir):
        for file_name in files:
            if file_name.find('.bag') > -1:
                file_path = os.path.join(roots, file_name)
                bag_list.append(file_path)

    return bag_list
def deal_perce_json(perce_path,eval_type,perce_json_path):
    bag_list = find_rosbag_path(perce_path)
    if eval_type == "front_fusion_dist":
        bag_list = [x for x in bag_list if x.find('fusion.bag')>-1]
    else:
        bag_list = [x for x in bag_list if x.find('perception.bag')>-1]
    dst = perce_json_path
    # if os.path.isdir(dst):
    #     shutil.rmtree(dst)
    os.makedirs(dst,exist_ok=True)
    if bag_list==[]:
        print('*****感知结果路径下未发现.bag结尾的rosbag包*****!!!')
    elif eval_type == "front_fusion_dist":
        for bag in bag_list:
            get_fusion_bag(bag,dst)
    elif eval_type in ['front_rp','side_rp','back_rp','barrier_front_rp','barrier_side_rp','barrier_back_rp','tl_rp','tsr_rp']:
        for bag in bag_list:
            get_detct_bag(bag,dst,eval_type)
    else:
        num = 0
        for bag in bag_list:
            num = get_bag_data(bag,dst,num,eval_type)
