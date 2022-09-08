import os
import json
import argparse
import cv2
import numpy as np

root_path = os.path.dirname(os.path.abspath(__file__))

# 定义图片所在路径
img_path_lf = os.path.join(root_path,  'ori_pic_1920x1280', 'side_left_front')
img_path_rf = os.path.join(root_path,  'ori_pic_1920x1280', 'side_right_front')
img_path_lr = os.path.join(root_path,  'ori_pic_1920x1280', 'side_left_rear')
img_path_rr = os.path.join(root_path,  'ori_pic_1920x1280', 'side_right_rear')
# 定义检测结果json文件所在路径
json_path_lf_detect = os.path.join(root_path, 'perce_json', 'side_left_front')
json_path_rf_detect = os.path.join(root_path, 'perce_json', 'side_right_front')
json_path_lr_detect = os.path.join(root_path, 'perce_json', 'side_left_rear')
json_path_rr_detect = os.path.join(root_path, 'perce_json', 'side_right_rear')
# 定义标注json文件所在路径
json_path_lf_label = os.path.join(root_path, 'lable_json', 'side_left_front')
json_path_rf_label = os.path.join(root_path, 'lable_json', 'side_right_front')
json_path_lr_label = os.path.join(root_path, 'lable_json', 'side_left_rear')
json_path_rr_label = os.path.join(root_path, 'lable_json', 'side_right_rear')
# 定义fusion_json文件所在路径
fusion_path_detect = os.path.join(root_path, 'perce_json', 'camera_fusion')

# 可视化结果图片存放文件夹
save_path = os.path.join(root_path, 'img_result')

# 定义图片的宽和高
resource_img_height = 1280
resource_img_width = 1920

# BEV图中定义中心点，注意，这里定义xy为车坐标系，x向前为正，y向左为正
# x_center_bev = 1080
# y_center_bev = 960
# 上行改为下行20220430
x_center_bev = (2500 / 2)
y_center_bev = (578 / 2)

# fusion图中定义中心点，注意，这里定义xy为车坐标系，x向前为正，y向左为正
# x_center_fusion = 1080
# y_center_fusion = 960
# 上行改为下行20220430
x_center_fusion = (2500 / 2)
y_center_fusion = (578 / 2)

# 所有标定框的长和宽，自己定义数值
width_bev = 60
length_bev = 170

# 检测json文件中的数值单位是米，所以对图框像素和米制之间转换,时间x范围是正负60米，y范围是正负30米
# x_conversion_coeff = (2160 / 130)
# y_conversion_coeff = (1920 / 30)
# 上行改为下行20220430
x_conversion_coeff = (2500 / 130)
y_conversion_coeff = (578 / 30)


def read_json_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def x_y_conversion(x, y):
    temp = x
    x = -y
    y = -temp
    return x, y


def draw_line(img, coor_1, coor_2):
    cv2.line(img, coor_1, coor_2, color=(170, 170, 170), thickness=2)


def load_detect_data(input_file):
    # 读取检测得到的2D数据
    x_detect = input_file['uv_bbox2d']['obstacle_bbox.x']
    y_detect = input_file['uv_bbox2d']['obstacle_bbox.y']
    h_detect = input_file['uv_bbox2d']['obstacle_bbox.height']
    w_detect = input_file['uv_bbox2d']['obstacle_bbox.width']
    obstacle_id = str(input_file['obstacle_id'])
    obstacle_type = str(input_file['obstacle_type'])

    # 数据需要加系数
    x_detect = int(np.round(x_detect * 3.75))
    # y_detect = int(np.round(y_detect * 3.75 + 48))
    # 上行改为下行20220430
    y_detect = int(np.round(y_detect * 3.75 + 200))
    h_detect = int(np.round(h_detect * 3.75))
    w_detect = int(np.round(w_detect * 3.75))

    # 读取BEV数据，读取的数据单位是米
    x_center_bev_detect = int(np.round(input_file['bbox3d']['obstacle_pos_x']))
    y_center_bev_detect = int(np.round(input_file['bbox3d']['obstacle_pos_y']))
    obstacle_length = input_file['obstacle_length']
    obstacle_width = input_file['obstacle_width']
    # 数据乘以系数
    x = int(np.round(x_center_bev_detect * x_conversion_coeff)) - x_center_bev
    y = int(np.round(y_center_bev_detect * y_conversion_coeff)) - y_center_bev
    # y = int(np.round(y_center_bev_detect * x_conversion_coeff)) - y_center_bev
    # 长宽由米制改为像素单位
    obstacle_length = obstacle_length * x_conversion_coeff
    # obstacle_width = obstacle_width * x_conversion_coeff
    # 上行改为下行
    obstacle_width = obstacle_width * y_conversion_coeff
    # xy坐标修改
    x, y = x_y_conversion(x, y)
    # 计算框的左上角和右下角
    x_min = int(x - obstacle_width / 2)
    y_min = int(y - obstacle_length / 2)
    x_max = int(x + obstacle_width / 2)
    y_max = int(y + obstacle_length / 2)
    return x_detect, y_detect, h_detect, w_detect, obstacle_id, obstacle_type, x_min, y_min, x_max, y_max


def load_label_data(input_file):
    x_label = int(np.round(input_file['box_2d']['x']))
    y_label = int(np.round(input_file['box_2d']['y']))
    w_label = int(np.round(input_file['box_2d']['w']))
    h_label = int(np.round(input_file['box_2d']['h']))
    id = str(input_file['id'])
    type = str(input_file['type'])

    # 修改，加下行代码20220430
    y_label = y_label

    # 读取标注的BEV数据
    x_center_bev_label = int(np.round(input_file['box_3d']['global_dists']['x']))
    y_center_bev_label = int(np.round(input_file['box_3d']['global_dists']['y']))
    # 乘以系数
    x = int(np.round(x_center_bev_label * x_conversion_coeff)) - x_center_bev
    y = int(np.round(y_center_bev_label * y_conversion_coeff)) - y_center_bev
    # xy方向交换
    x, y = x_y_conversion(x, y)
    # 计算框的左上角和右下角
    x_min = int(x - width_bev / 2)
    y_min = int(y - length_bev / 2)
    x_max = int(x + width_bev / 2)
    y_max = int(y + length_bev / 2)
    return x_label, y_label, w_label, h_label, id, type, x_min, y_min, x_max, y_max


def load_fusion_data(input_file):
    # 读取fusion_json文件中的xy坐标值
    x_filter = input_file['position']['obstacle_pos_x_filter']
    y_filter = input_file['position']['obstacle_pos_y_filter']
    length = input_file['obstacle_length']
    width = input_file['obstacle_width']
    id = str(input_file['obstacle_id'])
    type = str(input_file['obstacle_type'])

    # 计算读取的数值在图像上的坐标值
    # x = x_filter * x_conversion_coeff - x_center_fusion
    # y = y_filter * y_conversion_coeff - y_center_fusion

    x = x_filter * y_conversion_coeff - x_center_fusion
    y = y_filter * x_conversion_coeff - y_center_fusion
    length = length * x_conversion_coeff
    # width = width * x_conversion_coeff
    # 上行改为下行
    width = width * y_conversion_coeff

    # xy方向变换
    x, y = x_y_conversion(x, y)

    # 计算左上角和右下角
    x_min = int(np.round(x - width / 2))
    y_min = int(np.round(y - length / 2))
    x_max = int(np.round(x + width / 2))
    y_max = int(np.round(y + length / 2))
    return x_min, y_min, x_max, y_max, id, type


# 在分图上绘制检测内容
def draw_bbox_in_cicle_view(img, x1, y1, x2, y2, id, type, color):  # x2-w_detect    y2-h_detect
    # 在分图上绘检测框
    cv2.rectangle(img, (x1, y1), (x1 + x2, y1 + y2), color, 3)
    # 在分图上绘检测ID
    cv2.putText(img, 'ID:' + id, (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
    # 在分图上绘检测type
    cv2.putText(img, 'TYPE:' + type, (x1, y1 - 50), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)


def draw_bbox_in_bev(img, x1, y1, x2, y2, id, type, color):
    # 在BEV图上画框
    cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
    # 在BEV图上画检测ID
    cv2.putText(img, 'ID:' + id, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)
    # 在BEV图上画检测type
    cv2.putText(img, 'TYPE:' + type, (x1, y1 - 50), cv2.FONT_HERSHEY_PLAIN, 3, color, 2)


def main():
    imgs_num = len(os.listdir(img_path_lf))
    for i in range(imgs_num):
        # print(f'********** 进度：{i+1} / {imgs_num} **********')
        print('********** 进度：{} / {} **********'.format(i+1, imgs_num))

        # BEV图
        img_bev = np.zeros((2500, 578, 3), np.uint8)
        img_bev.fill(200)

        # 创建img_fusion_bev图
        img_fusion_bev = np.zeros((2500, 578, 3), np.uint8)
        img_fusion_bev.fill(200)

        '''
        left_front
        '''
        print('正在读取left_front数据...')


        json_file_lf_detect = os.listdir(json_path_lf_detect)
        json_file_lf_label = os.listdir(json_path_lf_label)
        json_file_lf_detect.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        json_file_lf_label.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        # 找到后缀是.bmp的图片
        imgs_lf = os.listdir(img_path_lf)

        # frame_vc6_18.png
        imgs_lf.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        # print(imgs_lf)
        img_name_lf = imgs_lf[i].split('.')[0]

        # 读取图片，并将图片改为np.array格式
        img_lf = cv2.imread(os.path.join(img_path_lf, imgs_lf[i]), 1)
        # img_lf = np.array(img_lf)

        # 遍历检测得到的json文件
        for json_file_detect in json_file_lf_detect:
            json_name_lf_detect = json_file_detect.split('.')[0]
            # 遍历标注jason文件
            for json_file_label in json_file_lf_label:
                json_name_lf_label = json_file_label.split('.')[0]
                if (img_name_lf == json_name_lf_detect) and (img_name_lf == json_name_lf_label):
                    # 读取检测得到的json文件参数
                    data_lf_detect = read_json_file(os.path.join(json_path_lf_detect, json_file_detect))
                    obstacle_lf_detect = data_lf_detect['tracks']

                    if obstacle_lf_detect == None:
                        continue

                    for obstacle_detect in obstacle_lf_detect:
                        x_detect, y_detect, h_detect, w_detect, \
                        obstacle_id, obstacle_type, \
                        x_min, y_min, x_max, y_max = load_detect_data(obstacle_detect)
                        # 在分图上绘检测检测内容
                        draw_bbox_in_cicle_view(img_lf, x_detect, y_detect, w_detect, h_detect, obstacle_id,
                                                obstacle_type, (0, 0, 255))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, obstacle_id, obstacle_type, (0, 0, 255))

                    # 读取标注的json文件参数
                    datas_lf_label = read_json_file(os.path.join(json_path_lf_label, json_file_label))
                    # 判断标注是否为空
                    if not datas_lf_label:
                        continue
                    for data_lf_label in datas_lf_label:
                        x_label, y_label, w_label, h_label, \
                        id, type, \
                        x_min, y_min, x_max, y_max = load_label_data(data_lf_label)
                        draw_bbox_in_cicle_view(img_lf, x_label, y_label, w_label, h_label, id, type, (0, 255, 0))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))
                        # 在fusion_bev图上绘制检测内容
                        draw_bbox_in_bev(img_fusion_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))

        '''
        right_front
        '''
        print('正在读取right_front数据...')

        json_file_rf_detect = os.listdir(json_path_rf_detect)
        json_file_rf_label = os.listdir(json_path_rf_label)
        json_file_rf_detect.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        json_file_rf_label.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))


        # 找到后缀是bmp的图片
        imgs_rf = os.listdir(img_path_rf)
        imgs_rf.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))

        img_name_rf = imgs_rf[i].split('.')[0]
        # 读取图片，更改图片格式为np.array
        img_rf = cv2.imread(os.path.join(img_path_rf, imgs_rf[i]), 1)
        # img_rf = np.array(img_rf)

        # 遍历检测得到的json文件
        for json_file_detect in json_file_rf_detect:
            json_name_rf_detect = json_file_detect.split('.')[0]
            # 遍历标注jason文件
            for json_file_label in json_file_rf_label:
                json_name_rf_label = json_file_label.split('.')[0]
                if (img_name_rf == json_name_rf_detect) and (img_name_rf == json_name_rf_label):
                    # 读取检测得到的json文件参数
                    data_rf_detect = read_json_file(os.path.join(json_path_rf_detect, json_file_detect))
                    obstacle_rf_detect = data_rf_detect['tracks']

                    if obstacle_rf_detect == None:
                        continue

                    for obstacle_detect in obstacle_rf_detect:
                        x_detect, y_detect, h_detect, w_detect, \
                        obstacle_id, obstacle_type, \
                        x_min, y_min, x_max, y_max = load_detect_data(obstacle_detect)
                        # 在分图上绘检测内容
                        draw_bbox_in_cicle_view(img_rf, x_detect, y_detect, w_detect, h_detect, obstacle_id,
                                                obstacle_type, (0, 0, 255))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, obstacle_id, obstacle_type, (0, 0, 255))

                    # 读取标注的json文件参数
                    datas_rf_label = read_json_file(os.path.join(json_path_rf_label, json_file_label))
                    # 判断是否为空
                    if not datas_rf_label:
                        continue
                    for data_rf_label in datas_rf_label:
                        x_label, y_label, w_label, h_label, \
                        id, type, \
                        x_min, y_min, x_max, y_max = load_label_data(data_rf_label)
                        # 在分图上绘标注数据
                        draw_bbox_in_cicle_view(img_rf, x_label, y_label, w_label, h_label, id, type, (0, 255, 0))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))
                        # 在fusion_bev图上绘制检测内容
                        draw_bbox_in_bev(img_fusion_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))

        '''
        left_rear
        '''
        print('正在读取left_rear数据...')

        json_file_lr_detect = os.listdir(json_path_lr_detect)
        json_file_lr_label = os.listdir(json_path_lr_label)
        json_file_lr_detect.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        json_file_lr_label.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))

        imgs_lr = os.listdir(img_path_lr)
        imgs_lr.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        img_name_lr = imgs_lr[i].split('.')[0]
        # 读取图片，更改图片格式为np.array
        img_lr = cv2.imread(os.path.join(img_path_lr, imgs_lr[i]), 1)
        # img_lr = np.array(img_lr)

        # 遍历检测得到的json文件
        for json_file_detect in json_file_lr_detect:
            json_name_lr_detect = json_file_detect.split('.')[0]
            # 遍历标注jason文件
            for json_file_label in json_file_lr_label:
                json_name_lr_label = json_file_label.split('.')[0]
                if (img_name_lr == json_name_lr_detect) and (img_name_lr == json_name_lr_label):
                    # 读取检测得到的json文件参数
                    data_lr_detect = read_json_file(os.path.join(json_path_lr_detect, json_file_detect))
                    obstacle_lr_detect = data_lr_detect['tracks']

                    if obstacle_lr_detect == None:
                        continue

                    for obstacle_detect in obstacle_lr_detect:
                        x_detect, y_detect, h_detect, w_detect, \
                        obstacle_id, obstacle_type, \
                        x_min, y_min, x_max, y_max = load_detect_data(obstacle_detect)
                        # 在分图上绘检测内容
                        draw_bbox_in_cicle_view(img_lr, x_detect, y_detect, w_detect, h_detect, obstacle_id,
                                                obstacle_type, (0, 0, 255))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, obstacle_id, obstacle_type, (0, 0, 255))

                    # 读取标注的json文件参数
                    datas_lr_label = read_json_file(os.path.join(json_path_lr_label, json_file_label))
                    # 判断是否为空
                    if not datas_lr_label:
                        continue
                    for data_lr_label in datas_lr_label:
                        x_label, y_label, w_label, h_label, \
                        id, type, \
                        x_min, y_min, x_max, y_max = load_label_data(data_lr_label)
                        # 在分图上绘标注数据
                        draw_bbox_in_cicle_view(img_lr, x_label, y_label, w_label, h_label, id, type, (0, 255, 0))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))
                        # 在fusion_bev图上绘制检测内容
                        draw_bbox_in_bev(img_fusion_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))

        '''
        right_rear
        '''
        print('正在读取right_rear数据...')

        json_file_rr_detect = os.listdir(json_path_rr_detect)
        json_file_rr_label = os.listdir(json_path_rr_label)
        json_file_rr_detect.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        json_file_rr_label.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))

        # 找到后缀是.bmp的图片
        imgs_rr = os.listdir(img_path_rr)
        imgs_rr.sort(key=lambda x: (x.split('.')[0].split('_')[-1].zfill(6)))
        img_name_rr = imgs_rr[i].split('.')[0]

        # 读取图片，更改图片格式为np.array
        img_rr = cv2.imread(os.path.join(img_path_rr, imgs_rr[i]), 1)
        img_rr = np.array(img_rr)

        # 遍历检测得到的json文件
        for json_file_detect in json_file_rr_detect:
            json_name_rr_detect = json_file_detect.split('.')[0]
            # 遍历标注jason文件
            for json_file_label in json_file_rr_label:
                json_name_rr_label = json_file_label.split('.')[0]
                if (img_name_rr == json_name_rr_detect) and (img_name_rr == json_name_rr_label):
                    # 读取检测得到的json文件参数
                    data_rr_detect = read_json_file(os.path.join(json_path_rr_detect, json_file_detect))
                    obstacle_rr_detect = data_rr_detect['tracks']

                    if obstacle_rr_detect == None:
                        continue

                    for obstacle_detect in obstacle_rr_detect:
                        x_detect, y_detect, h_detect, w_detect, \
                        obstacle_id, obstacle_type, \
                        x_min, y_min, x_max, y_max = load_detect_data(obstacle_detect)
                        # 在分图上绘检测内容
                        draw_bbox_in_cicle_view(img_rr, x_detect, y_detect, w_detect, h_detect, obstacle_id,
                                                obstacle_type, (0, 0, 255))
                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, obstacle_id, obstacle_type, (0, 0, 255))


                    # 读取标注的json文件参数
                    datas_rr_label = read_json_file(os.path.join(json_path_rr_label, json_file_label))

                    # 判断是否为空
                    if not datas_rr_label:
                        continue
                    for data_rr_label in datas_rr_label:
                        x_label, y_label, w_label, h_label, \
                        id, type, \
                        x_min, y_min, x_max, y_max = load_label_data(data_rr_label)

                        # 在分图上绘标注数据
                        draw_bbox_in_cicle_view(img_rr, x_label, y_label, w_label, h_label, id, type, (0, 255, 0))

                        # 在BEV图上绘制检测内容
                        draw_bbox_in_bev(img_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))

                        # 在fusion_bev图上绘制检测内容
                        draw_bbox_in_bev(img_fusion_bev, x_min, y_min, x_max, y_max, id, type, (0, 255, 0))

        # fusion图像
        # fusion_path_detect = os.path.join(root_path, 'image_record', 'image_record_json', 'fusion')
        # 读取fusion文件
        fusion_files = os.listdir(fusion_path_detect)
        fusion_files.sort(key=lambda x: x.split('.')[0])
        for fusion_file in fusion_files:
            data_fusion_detect = read_json_file(os.path.join(fusion_path_detect, fusion_file))
            fusion_file_name = fusion_file.split('.')[0]
            if img_name_rr.rsplit('_')[-1] == fusion_file_name:
                obstacle_fusion_detect = data_fusion_detect['tracks']

                if obstacle_fusion_detect == None:
                    continue

                for obstacle_detect in obstacle_fusion_detect:
                    x_min, y_min, x_max, y_max, id, type = load_fusion_data(obstacle_detect)
                    # 在fusion_bev图上绘制检测内容
                    draw_bbox_in_bev(img_fusion_bev, x_min, y_min, x_max, y_max, id, type, (0, 0, 255))






        # 在fusion_bev图上画上框和中间竖线
        cv2.rectangle(img_fusion_bev, (0, 0), (578, 2500), (0, 0, 255), 2)
        cv2.line(img_fusion_bev, (int(578 / 2), 0), (int(578 / 2), 2500), (0, 0, 0), 2)
        # 竖向网格线
        for m in range(0, 8):
            draw_line(img_fusion_bev, (36 + m * 72, 0), (36 + m * 72, 2500))
        # 横向网格线
        for m in range(13):
            if m == 6:
                cv2.line(img_fusion_bev, (0, 1250), (578, 1250), color=(0, 0, 0), thickness=2)
            else:
                draw_line(img_fusion_bev, (0, 98 + m * 192), (554, 98 + m * 192))

        # 在img_bev图上画上框和中间竖线
        cv2.rectangle(img_bev, (0, 0), (578, 2500), (0, 0, 255), 2)
        cv2.line(img_bev, (int(578 / 2), 0), (int(578 / 2), 2500), color=(0, 0, 0), thickness=2)
        # 竖向网格线
        for m in range(0, 8):
            draw_line(img_bev, (36 + m * 72, 0), (36 + m * 72, 2500))
        # 横向网格线
        for m in range(13):
            if m == 6:
                cv2.line(img_bev, (0, 1250), (578, 1250), color=(0, 0, 0), thickness=2)
            else:
                draw_line(img_bev, (0, 98 + m * 192), (554, 98 + m * 192))

        # 在十字线中间画框表示本车
        cv2.rectangle(img_bev, (270, 1202), (308, 1298), (0, 0, 0), 2)
        cv2.rectangle(img_fusion_bev, (270, 1202), (308, 1298), (0, 0, 0), 2)

        # 单独画个细条图用于写字
        img_words = np.zeros((60, 578 * 2, 3), np.uint8)
        img_words.fill(200)
        cv2.rectangle(img_words, (0, 0), (578 * 2, 60), (0, 0, 255), 2)
        cv2.line(img_words, (578, 0), (578, 60), color=(0, 0, 255), thickness=2)
        cv2.putText(img_words, 'circle_bev', (200, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)
        cv2.putText(img_words, 'fusion_bev', (750, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 2)

        # 将四路图组合在一起
        print('正在拼四路图中...')
        img_left = np.vstack([np.hstack([img_lf, img_rf]), np.hstack([img_lr, img_rr])])

        print('正在拼BEV图中...')
        # img_down = np.hstack([img_bev, img_fusion_bev])
        # img_down = np.vstack([img_words, np.hstack([img_bev, img_fusion_bev])])
        img_right_down = np.hstack([img_bev, img_fusion_bev])

        print('正在拼总图中...')
        # img = np.vstack([img_upper, img_words])
        # img = np.vstack([img, img_down])
        # img = np.vstack([img_upper, img_down])
        img_right = np.vstack([img_words, img_right_down])
        img = np.hstack([img_left, img_right])

        # 保存
        print('正在保存中...')
        # img_path = os.path.join(save_path, str(i)+'.png')
        img_path = os.path.join(save_path, img_name_lf + '.png')

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        cv2.imwrite(img_path, img)

    print('完成！')


if __name__ == '__main__':
    main()
