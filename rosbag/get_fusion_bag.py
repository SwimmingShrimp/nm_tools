from turtle import distance
import rosbag
import os

def get_fusion_bag(fusion_bag,dst):
    bag_data = rosbag.Bag(fusion_bag,'r')
    topic_list = ["/perception/obstacle_list","/fusion/obstacle_list"]
    bag_data = bag_data.read_messages(topic_list)
    bag_data_list = [[msg_type, msg, time_stamp] for msg_type, msg, time_stamp in bag_data]

    latest_camera_obstacle_array = []
    seq = -1
    for bag_data in bag_data_list:
        if (bag_data[0] == "/perception/obstacle_list"):
            seq = bag_data[1].header.seq
            latest_camera_obstacle_array = bag_data[1].tracks
        if (bag_data[0] == "/fusion/obstacle_list"):
            json_data_list =[]
            for fused_obstacle in bag_data[1].tracks:
                match_camera_obs_id = fused_obstacle.associate_infos[0].id
                if (match_camera_obs_id != 0):
                    for camera_obstacle in latest_camera_obstacle_array:
                        if camera_obstacle.id == match_camera_obs_id:
                            stamp = fused_obstacle.associate_infos[1].stamp.secs
                            if int(stamp)==0:
                                continue
                            distance = {
                                "x":fused_obstacle.associate_infos[1].position.x,
                                "y":fused_obstacle.associate_infos[1].position.y
                            }
                            camera_id = camera_obstacle.camera_position
                            if camera_id==1:
                                camera_id=0
                            elif camera_id==2:
                                camera_id=1
                            type = camera_obstacle.type
                            box_2d = {
                                "x":camera_obstacle.uv_bbox2d.left_top.x,
                                "y":camera_obstacle.uv_bbox2d.left_top.y,
                                "w":camera_obstacle.uv_bbox2d.size.x,
                                "h":camera_obstacle.uv_bbox2d.size.y
                            }
                            box_3d = {
                                "l":camera_obstacle.bbox3d.size.x,
                                "w":camera_obstacle.bbox3d.size.y,
                                "h":camera_obstacle.bbox3d.size.z
                            }
                            yaw = camera_obstacle.rotation.yaw
                            json_content = {
                                "type":type,
                                "box_2d":box_2d,
                                "box_3d":box_3d,
                                "distance":distance,
                                "yaw":yaw,
                                "camera_id":camera_id
                            }
                            json_data_list.append(json_content)
        utils.write_json_data(os.path.join(dst,json_name),json_data)
        
                            
                        
fusion_bag = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/06_data/result/fusion.bag'
dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/06_data/result/fusion'
os.makedirs(dst,exist_ok=True)
get_fusion_bag(fusion_bag,dst)

