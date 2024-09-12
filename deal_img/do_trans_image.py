import cv2
import numpy as np
import copy
import math
import json
degree2rad = np.pi / 180
from scipy.spatial.transform import Rotation
from PIL import Image, ImageDraw, ImageFont


def do_trans_image(view, image,json_data):
    camera_param=get_camera_param(json_data,'front_near')
    label_to_replay=get_label_replay_map(camera_param, 'front_near')
    # 将标注图片映射到回灌图片
    map1, map2 = label_to_replay["mapx"],label_to_replay["mapy"]
    img_distort = cv2.remap(image, map1, map2, cv2.INTER_LINEAR)
    return img_distort


def get_label_replay_map(camera_param, view):
    # 标注图片到回灌图片的映射关系
    w = camera_param.width
    h = camera_param.height
    fov = camera_param.fov
    new_camera_matrix = get_new_camera_param_matrix(camera_param.intrinsics, w, fov)
    K = np.zeros(8)
    RCc =get_RCc(camera_param, view) # if use_extrinsic_rectify else None
    map1, map2 = cv2.initUndistortRectifyMap(new_camera_matrix, K, RCc, camera_param.virtual_intrinsics, (w, h),
                                             cv2.CV_32FC1)
    ret = {
        "mapx": map1,
        "mapy": map2
    }
    return ret

def get_new_camera_param_matrix(intrinsics,w,fov):
    new_camera_param = copy.deepcopy(intrinsics)
    new_fx = w/(2 * math.tan(fov * degree2rad/2))
    new_camera_param[0][0] = new_fx
    new_camera_param[1][1] = new_fx
    return new_camera_param

def get_camera_param(json_data,camera_name):
        # 从文本中读取相机参数
        try:
            camera_param_dict = json_data[camera_name]
            rot_x_alfa = camera_param_dict['orin_camera_param']['extrinsics']['rot_x_alfa']
            rot_y_beta = camera_param_dict['orin_camera_param']['extrinsics']['rot_y_beta']
            rot_z_gama = camera_param_dict['orin_camera_param']['extrinsics']['rot_z_gama']
            trans_x0= camera_param_dict['orin_camera_param']['extrinsics']['trans_x0']
            trans_y0= camera_param_dict['orin_camera_param']['extrinsics']['trans_y0']
            trans_z0= camera_param_dict['orin_camera_param']['extrinsics']['trans_z0']
            fx = camera_param_dict['orin_camera_param']['intrinsics']['fx']
            fy = camera_param_dict['orin_camera_param']['intrinsics']['fy']
            cx = camera_param_dict['orin_camera_param']['intrinsics']['cx']
            cy = camera_param_dict['orin_camera_param']['intrinsics']['cy']
            k1 = camera_param_dict['orin_camera_param']['distortions']['k1']
            k2 = camera_param_dict['orin_camera_param']['distortions']['k2']
            p1 = camera_param_dict['orin_camera_param']['distortions']['p1']
            p2 = camera_param_dict['orin_camera_param']['distortions']['p2']
            k3 = camera_param_dict['orin_camera_param']['distortions']['k3']
            k4 = camera_param_dict['orin_camera_param']['distortions']['k4']
            k5 = camera_param_dict['orin_camera_param']['distortions']['k5']
            k6 = camera_param_dict['orin_camera_param']['distortions']['k6']
            fx_new = camera_cut_info[camera_name]['default_new_cam_mtx']['fx']
            fy_new = camera_cut_info[camera_name]['default_new_cam_mtx']['fy']
            cx_new = camera_cut_info[camera_name]['default_new_cam_mtx']['cx']
            cy_new = camera_cut_info[camera_name]['default_new_cam_mtx']['cy']

            width = camera_param_dict["width"]
            height = camera_param_dict["height"]
            fov = camera_param_dict["fov"]
        except Exception as e:
            raise str(e)
        intrinsics = np.array([[fx, 0, cx],
                               [0, fy, cy],
                               [0, 0, 1]])
        distortions = np.array([k1, k2, p1, p2, k3, k4, k5, k6])

        virtual_intrinsics = np.array([[fx_new, 0, cx_new],
                                       [0, fy_new, cy_new],
                                       [0, 0, 1]])
        extrinsics = np.array([rot_x_alfa, rot_y_beta, rot_z_gama, trans_x0, trans_y0, trans_z0])

        camera_param = CameraParam(extrinsics, intrinsics, distortions, virtual_intrinsics,width,height,fov)
        return camera_param
def get_RCc(camera_param, view):
    if view == "back_middle":
        RCw = construct_rot_x(np.pi / 2).dot(construct_rot_y(0)).dot(construct_rot_z(-np.pi / 2))
    elif view.startswith("front"):
        RCw = construct_rot_x(np.pi / 2).dot(construct_rot_y(0)).dot(construct_rot_z(np.pi / 2))
    elif view.startswith("side"):
        RCw = None
    else:
        raise ValueError(f"camera name is {view}, please check camera name")
    extrinsics = camera_param.extrinsics
    Rwc = construct_rot_z(-extrinsics[2] * degree2rad).dot(
        construct_rot_y(-extrinsics[1] * degree2rad)).dot(construct_rot_x(-extrinsics[0] * degree2rad))
    if RCw is None:
        RCc = None
    else:
        RCc = RCw.dot(Rwc)
    return RCc

def construct_rot_x(alpha):
    return np.array([[1.0, 0.0, 0.0],
                     [0.0, math.cos(alpha), -math.sin(alpha)],
                     [0.0, math.sin(alpha), math.cos(alpha)]])
def construct_rot_y(beta):
    return np.array([[math.cos(beta), 0.0, math.sin(beta)],
                     [0.0, 1.0, 0.0],
                     [-math.sin(beta), 0.0, math.cos(beta)]])
def construct_rot_z(gamma):
    return np.array([[math.cos(gamma), -math.sin(gamma), 0.0],
                     [math.sin(gamma), math.cos(gamma), 0.0],
                     [0.0, 0.0, 1.0]])
class CameraParam():
    def __init__(self, extrinsics,intrinsics,distortions, virtual_intrinsics,width,height,fov):
        self.extrinsics = extrinsics
        self.intrinsics = intrinsics
        self.distortions = distortions
        self.virtual_intrinsics = virtual_intrinsics
        self.width = width
        self.height = height
        self.fov = fov

camera_cut_info = {
    "front_far":{
        "mult_x": 3.75,
        "mult_y": 3.75,
        "bottom_cut": 180,
        "top_cut": 180,
        "fx": 7230.0,
        "left_cut": 0,
        "right_cut": 0,
        "fov": 30,
        "pixel_x": 3840,
        "pixel_y": 2160,
        "default_new_cam_mtx": {
        "fx": 7230.0,
        "fy": 7230.0,
        "cx": 1920,
        "cy": 1080
        }
    },
    "front_near":{
        "mult_x": 5,
        "mult_y": 5,
        "bottom_cut": 0,
        "top_cut": 240,
        "fx": 1911,
        "left_cut": 0,
        "right_cut": 0,
        "fov": 120,
        "pixel_x": 3840,
        "pixel_y": 2160,
        "default_new_cam_mtx": {
            "fx": 1911.0,
            "fy": 1911.0,
            "cx": 1920,
            "cy": 1080
        }
    },
    "back_middle":{
        "mult_x": 5,
        "mult_y": 5,
        "bottom_cut": 0,
        "top_cut": 240,
        "fx": 1911,
        "left_cut": 0,
        "right_cut": 0,
        "fov": 60,
        "pixel_x": 3840,
        "pixel_y": 2160,
        "default_new_cam_mtx": {
            "fx": 1911.0,
            "fy": 1911.0,
            "cx": 1920,
            "cy": 1080
        }
    },
    "side_left_rear":{
        "mult_x":2.5,
        "mult_y":2.5,
        "top_cut":120,
        "bottom_cut": 0,
        "left_cut":0,
        "right_cut": 0,
        "fov": 100,
        "fx": 1190,
        "pixel_x": 1920,
        "pixel_y": 1080,
        "default_new_cam_mtx": {
            "fx": 1186.0185617715579,
            "fy": 1186.286525612066,
            "cx": 930.3223800454065,
            "cy": 484.70633526593014
        }
    },
    "side_left_front":{
        "mult_x":2.5,
        "mult_y":2.5,
        "top_cut":120,
        "bottom_cut": 0,
        "left_cut":0,
        "right_cut": 0,
        "fov": 100,
        "fx": 1190,
        "pixel_x": 1920,
        "pixel_y": 1080,
        "default_new_cam_mtx": {
            "fx": 1188.9596625733955,
            "fy": 1188.2316441742923,
            "cx": 931.7555346569334,
            "cy": 493.2107368346228
        }
    },
    "side_right_front":{
        "mult_x":2.5,
        "mult_y":2.5,
        "top_cut":120,
        "bottom_cut": 0,
        "left_cut":0,
        "right_cut": 0,
        "fov": 100,
        "fx": 1190,
        "pixel_x": 1920,
        "pixel_y": 1080,
        "default_new_cam_mtx": {
            "fx": 1192.0083280230208,
            "fy": 1190.072477402353,
            "cx": 925.3813348334672,
            "cy": 517.2386461549992
        },
    },
    "side_right_rear":{
        "mult_x":2.5,
        "mult_y":2.5,
        "top_cut":120,
        "bottom_cut": 0,
        "left_cut":0,
        "right_cut": 0,
        "fov": 100,
        "fx": 1190,
        "pixel_x": 1920,
        "pixel_y": 1080,
        "default_new_cam_mtx": {
            "fx": 1193.5190471084595,
            "fy": 1193.292263527134,
            "cx": 930.5146454411819,
            "cy": 488.8136042309725
        }
    }
}

# 定义一个函数用于加载 JSON 文件数据
def get_json_data(json_file):
    with open(json_file) as f:
        try:
            json_data = json.load(f)  # 尝试加载 JSON 文件数据
        except:
            print('json文件加载失败：{}'.format(json_file))  # 如果加载失败，打印错误信息
            return {}  # 返回空字典
        return json_data  # 成功加载则返回 JSON 数据


