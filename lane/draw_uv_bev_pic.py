'''
Author: lixialin lixialin@nullmax.ai
Date: 2024-04-10 17:46:21
LastEditors: lixialin lixialin@nullmax.ai
LastEditTime: 2024-04-23 11:46:29
'''
'''
Author: lixialin lixialin@nullmax.ai
Date: 2024-02-18 10:49:06
LastEditors: lixialin lixialin@nullmax.ai
LastEditTime: 2024-04-10 17:46:24
'''
import rosbag
import os
import cv2
import numpy as np
import shutil
from moviepy.editor import ImageClip,VideoFileClip
import sys
sys.path.append('../')
import utils




def draw_pic(json_save_path,img_save_path,new_img_save_path,ext_arr,K):
    # 获取json文件列表
    json_list = [os.path.join(json_save_path,i) for i in sorted(os.listdir(json_save_path)) if i.endswith('.json')]
    # 画车道线的颜色
    color = (255,255,0)
    # bev图的尺寸
    bev_x = 512
    bev_y = 80
    # 假设车位线的画的范围是，纵向160m,横向20m
    x_conversion_coeff = (bev_x / 160)
    y_conversion_coeff = (bev_y / 20)
    for json_file in json_list:
        data = utils.get_json_data(json_file)
        filename = str(os.path.basename(json_file).split('.')[0])
        if data["lane_list"]:
            # 创建一个空白图片
            bev_pic = np.zeros((bev_x,bev_y,3),dtype=np.uint8)
            camera_pic = cv2.imread(os.path.join(img_save_path,filename+'.jpg'))
            # 开始按顺序画每一条车道线           
            for lane_data in data["lane_list"]:
                c0 = lane_data["c0"]
                c1 = lane_data["c1"]
                c2 = lane_data["c2"]
                view_range_start = lane_data["view_range_start"]
                view_range_end = lane_data["view_range_end"]
                # 根据车道线的开始位置和结束位置，纵向等间隔找到piece_num个点，最少10个的点
                if abs(view_range_end-view_range_start)>10 :
                    piece_num = abs(int((view_range_end-view_range_start)/1))
                else:
                    piece_num = 10
                x = np.linspace(view_range_start, view_range_end, piece_num)
                # 根据c0,c1,c2,c3生成一个3次多项式
                coeff = np.array([c2,c1,c0],np.float32)
                poly = np.poly1d(coeff)
                # 根据多项式，计算每个点的y值
                y = poly(x)
                '''在空白图片上画bev图'''
                # 坐标系转换：车体坐标系转换成u坐标系
                # 车体坐标系:圆点是O1，x轴向前，y轴向左；但是平台实际输出融合结果时，x轴向前，y轴向右
                # uv坐标系:圆点是O2,X轴和Y轴方向相反，所以在后面point中xy做了交换
                #    O2---------------->Y
                #    |     x    |
                #    |     |    |
                #    |     |    |
                # y<-|-----O1------
                #    |
                #    X
                new_x = bev_x - x * x_conversion_coeff
                new_y = bev_y/2 - (-y * y_conversion_coeff)
                points = list(zip(new_y, new_x))
                cv2.polylines(bev_pic,[np.array(points, np.int32)], False, color=color, thickness=1)
                '''在相机图片上画lane'''
                Pws = list(zip(x, y))
                Pws = np.array([[i[0],i[1],0,1] for i in Pws],dtype=np.float32)   # (n*4)
                matrix = K @ np.linalg.inv(ext_arr)  # (3,4)
                Pps = np.array([np.dot(matrix,np.transpose(i)) for i in Pws])  #(3,n)
                Pps = np.array([[i[0]/i[2],i[1]/i[2]] for i in Pps ], dtype=np.int32)  #(2,n)
                Pps = np.array([i for i in Pps if 0<i[0]<768 and 0<i[1]<512])   # 过滤超出uv图片大小的车道线点
                cv2.polylines(camera_pic, [Pps], False, color=color, thickness=2)

            '''bev图+相机图左右拼接,并保存图片'''
            pic = cv2.hconcat([camera_pic,bev_pic])    
            save_img_file = os.path.join(new_img_save_path,filename+'.jpg')
            cv2.imwrite(save_img_file,pic)

def ros_2_json(json_save_path,bag_file):    
    bag_data = rosbag.Bag(bag_file,'r')
    lane_data = bag_data.read_messages(["/perception/lka_lane_list"])    
    for topic,msg, t in lane_data:   
        if msg:
            lane_list = [{
                "position":lane_.position,
                "type":lane_.type,
                "quality":lane_.quality,
                "color":lane_.color,
                "c0":lane_.position_parameter_c0, 
                "c1":lane_.heading_angle_parameter_c1,
                "c2":lane_.curvature_parameter_c2,
                "view_range_start":lane_.view_range_start,
                "view_range_end":lane_.view_range_end} for lane_ in msg.lanes]
            
        utils.write_json_data(os.path.join(json_save_path,str(msg.header.seq)+'.json'),{"lane_list":lane_list})

# def analyse_img(json_save_path,video_path,img_save_path):
    # json_name_list = [str(i.split('.')[0]) for i in os.listdir(json_save_path) if i.endswith('.json')]
    # json_name_start = int(json_name_list[0])
    # json_length = len(json_name_list)
    # clip = VideoFileClip(video_path)
    # for i in range(json_name_start,json_name_start+json_length):
    #     frame = clip.get_frame(i)
    #     frame.save_frame(os.path.join(img_save_path,str(i)+'.jpg'))
    # clip.close()
    


if __name__ == "__main__":
    json_save_path = "/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/result/test/json"    
    bag_file = '/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/p0/demo_HU-BTN957_2024-03-20-14-52-03_1.bag'
    video_path = '/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/p0/front_near/front_near.mp4'
    img_save_path = '/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/result/test/img'
    new_img_save_path = '/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/result/test/new_img'
    
    '''将bag包转成json'''
    # if os.path.exists(json_save_path):
    #     shutil.rmtree(json_save_path)
    # os.makedirs(json_save_path,exist_ok=True)
    # ros_2_json(json_save_path,bag_file)

    '''根据json解析视频对应帧为图片'''
    # if os.path.exists(img_save_path):
    #     shutil.rmtree(img_save_path)
    # os.makedirs(img_save_path,exist_ok=True)
    # analyse_img(json_save_path,video_path,img_save_path)

    '''获取内外参矩阵'''
    calibration_param = "/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/p0/config/camera/front_near/calibration_param.json"
    ldc_param = "/media/ubuntu/b4228689-0850-4159-ad34-8eaba32c783d/data_temp/p0/config/camera/front_near/ldc_param.json"
    ext_arr = utils.get_json_data(calibration_param)["extrinsics"]
    int_arr_file = utils.get_json_data(ldc_param)["main_roi"]["undist_intrinsic"]
    fx = int_arr_file["fx"]
    fy = int_arr_file["fy"]
    cx = int_arr_file["cx"]
    cy = int_arr_file["cy"]
    K = [[fx,0,cx,0],[0,fy,cy,0],[0,0,1,0]]

    ''''将感知结果分别画到model_input图和bev图片上'''
    if os.path.exists(new_img_save_path):
        shutil.rmtree(new_img_save_path)
    os.makedirs(new_img_save_path,exist_ok=True)
    draw_pic(json_save_path,img_save_path,new_img_save_path,ext_arr,K)
