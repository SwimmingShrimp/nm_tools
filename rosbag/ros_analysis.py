from ast import mod
import rosbag
import pandas as pd
import os
import cv2

enum_obstacle3= {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',
                      7: 'tricycle',8: 'misc',9:'cone', 10:'barrier', 11:'safety-crash-barrels',
                      12:'tripod', 13:'traffic_light', 14:'traffic_sign',15:'parking_lock',16:'wheel',17:'speed_bump',18:'stop_block'}
def dist(bag_list,rosbag_path,dst):
    topic_list = ["/perception/obstacle_list","/fusion/obstacle_list"]
    result = []
    for bagfile in bag_list:
        bag_data = rosbag.Bag(os.path.join(rosbag_path,bagfile))
        bag_data = bag_data.read_messages(topic_list)
        bag_data_list = [[msg_type, msg, time_stamp] for msg_type, msg, time_stamp in bag_data] 
        temp_cam_frame_list = []
        for bag_data_ in bag_data_list:
            if (bag_data_[0] == "/perception/obstacle_list"):
                # 用于保存10帧的视觉pb消息
                temp_cam_frame_list.append(bag_data_[1])
                if len(temp_cam_frame_list) > 10:
                    temp_cam_frame_list.pop(0)
            # # 找到一帧融合
            if (bag_data_[0] == "/fusion/obstacle_list"):
                # 对于该帧融合中所有的障碍物
                for fused_obstacle in bag_data_[1].tracks:
                    fusion_id = fused_obstacle.id
                    distx = abs(fused_obstacle.position.x)
                    if 160>distx>=150:
                        match_camera_obs_id = fused_obstacle.associate_infos[0].id
                        # 取出该融合对应的视觉的时间戳
                        ass_camera_time_stamp_secs = fused_obstacle.associate_infos[0].stamp.secs
                        ass_camera_time_stamp_nsecs = fused_obstacle.associate_infos[0].stamp.nsecs
                        # print(bagfile,distx,fusion_id,match_camera_obs_id,ass_camera_time_stamp_secs,ass_camera_time_stamp_nsecs)
                        # 从上面保存的视觉的list中找到对应的帧
                        for cam_obs_frame in temp_cam_frame_list:
                            if cam_obs_frame.send_time.secs == ass_camera_time_stamp_secs and \
                                cam_obs_frame.send_time.nsecs  == ass_camera_time_stamp_nsecs:
                                frame_id = cam_obs_frame.header.seq
                                # 找到对应的视觉障碍物
                                for cam_track in cam_obs_frame.tracks:
                                    if match_camera_obs_id == cam_track.id:
                                        camera_id = cam_track.camera_position
                                        camera_2d_x = round(cam_track.uv_bbox2d.left_top.x,3)
                                        camera_2d_y = round(cam_track.uv_bbox2d.left_top.y,3)
                                        camera_2d_w = round(cam_track.uv_bbox2d.size.x,3)
                                        camera_2d_h = round(cam_track.uv_bbox2d.size.y,3)
                                        result.append([frame_id,fusion_id,match_camera_obs_id,camera_id,camera_2d_x,camera_2d_y,camera_2d_w,camera_2d_h])
                                continue    
    df = pd.DataFrame(result,columns=["frame_id","fusion_id","match_camera_obs_id",\
        "camera_id","camera_2d_x","camera_2d_y","camera_2d_w","camera_2d_h"])
    df.to_excel('{}/dist_vel.xlsx'.format(dst),sheet_name='process_data')
    # df.loc[(abs(df['radar_dist_x']) >= 0) & (abs(df['radar_dist_x']) <40),'纵向区间'] = 1
    # df.loc[(abs(df['radar_dist_x']) >= 40) & (abs(df['radar_dist_x']) <80),'纵向区间'] = 2
    # df.loc[(abs(df['radar_dist_x']) >= 80),'纵向区间'] = 3
    # df.to_excel('{}/dist_vel.xlsx'.format(dst),sheet_name='process_data')
    # all_data = pd.read_excel('{}/dist_vel.xlsx'.format(dst),sheet_name='process_data')
    # all_data["数量"] = 1
    # df2 = all_data.groupby(['obstacle_type','纵向区间']).agg({'数量':'sum','dist_x':'mean','dist_y':'mean','vel_x':'mean','vel_y':'mean',})        
    # df_dist_x =df.loc[((df["radar_dist_x"]<=5)&(df["dist_x"]>2)) | ((df["radar_dist_x"]>5)&(df["dist_x_rate"]>1))]
    # df_dist_y =df.loc[(df["dist_y"]>2)]
    # df_vel_x = df.loc[((df["radar_vel_x"]<=10)&(df["vel_x"]>3)) | ((df["radar_vel_x"]>10)&(df["vel_x_rate"]>1))]
    # df_vel_y =df.loc[(df["vel_y"]>2)]
    # with pd.ExcelWriter('{}/dist_vel.xlsx'.format(dst), mode='a',engine="openpyxl") as writer:
    #     df2.to_excel(writer, sheet_name='summary')
    #     df_dist_x.to_excel(writer, sheet_name='纵向测距偏差数据')
    #     df_dist_y.to_excel(writer, sheet_name='横向测距偏差数据')
    #     df_vel_x.to_excel(writer, sheet_name='纵向测速偏差数据')
    #     df_vel_y.to_excel(writer, sheet_name='横向测速偏差数据')

def generate_json():
    pass


def draw_pic(rosbag_path,model_input_path,dst,model_input_dir):
    df = pd.read_excel('{}/dist_vel.xlsx'.format(dst),sheet_name='纵向测距偏差数据',index_col=0)
    for key,value in df.groupby(['frame_id','camera_id']):
        frame_id = value.iloc[0]['frame_id']
        camera_name = config.front_config["camera_position"][value.iloc[0]['camera_id']]
        if camera_name in model_input_dir:
            for i in range(0,len(value)):
                pass
                

    # for i in range(0,len(df)):
    #     frame_id = df.iloc[i]['frame_id']
    #     camera_name = config.front_config["camera_position"][df.iloc[i]['camera_id']]
    #     img = cv2.imread(os.path.join(model_input_dir,camera_name,str(frame_id)+'.jpg'))
    #     camera_2d_x = int(df.iloc[i]['camera_2d_x'])
    #     camera_2d_y = int(df.iloc[i]['camera_2d_y'])
    #     camera_2d_w = int(df.iloc[i]['camera_2d_w'])
    #     camera_2d_h = int(df.iloc[i]['camera_2d_h'])
    #     camera_dist_x = df.iloc[i]['camera_dist_x']
    #     radar_dist_x = df.iloc[i]['radar_dist_x']
    #     radar_2d_x = int(df.iloc[i]['radar_2d_x'])
    #     radar_2d_y = int(df.iloc[i]['radar_2d_y'])
    #     radar_2d_w = int(df.iloc[i]['radar_2d_w'])
    #     radar_2d_h = int(df.iloc[i]['radar_2d_h'])

    
    



if __name__ == "__main__":
    rosbag_path = '/home/lixialin/Downloads/data/rosbag'
    model_input_path = '/home/lixialin/Downloads/data/model_input_frame'
    camera_name_list = ["front_far","front_near","back_middle","side_left_front","side_left_rear","side_right_front","side_right_rear"]
    dst = os.path.dirname(rosbag_path)
    bag_file = os.listdir(rosbag_path)
    bag_list = [x for x in bag_file if x.endswith('.bag')]

    dist(bag_list,rosbag_path,dst)
    # 融合上毫米波雷达的障碍物的测距测速分析
    # dist_vel(bag_list,rosbag_path,dst)
    # dir_list = os.listdir(model_input_path)
    # model_input_dir = []
    # [model_input_dir.append(x) for x in dir_list if x in camera_name_list]
    # [os.makedirs(x) for x in dir_list if x in camera_name_list]
    # draw_pic(rosbag_path,model_input_path,dst,model_input_dir)
    
    # 车道线颜色/类型跳变的分析
    


