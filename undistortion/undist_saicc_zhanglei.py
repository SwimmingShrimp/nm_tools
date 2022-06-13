import imghdr
import cv2
import math as m
import numpy as np
import matplotlib.pyplot as plt

def undist_cvundistort(orig_image, cam_params):

    cam_intrin = np.array([[cam_params["fx"], 0, cam_params["cx"]], 
                           [0, cam_params["fy"], cam_params["cy"]],
                           [0, 0, 1]])

    if len(cam_params.keys()) <= 8:
        dist_coef = np.array([cam_params['k1'], cam_params['k2'], cam_params['p1'], cam_params['p2']])
    else:
        dist_coef = np.array([cam_params['k1'], cam_params['k2'], cam_params['p1'], cam_params['p2'],
                              cam_params['k3'], cam_params['k4'], cam_params['k5'], cam_params['k6']])    
                        
    dst_image = cv2.undistort(orig_image, cam_intrin, dist_coef, None, cam_intrin)
    return dst_image, cam_intrin

if __name__ == "__main__":
    data_root = "/data1/NMtest/DataChoice/ShangQi/20220426/dataset_merge/Feb"
    dst = "/data1/NMtest/DataChoice/ShangQi/20220426/dataset_undist/Feb_c"
    camera_index = 0
    '''saic,1月份数据去畸变内参'''
    # intrin_dict = {
    #     0 : {"fx": 980.3544386371, "fy": 980.1134261942, "cx": 966.2492021282,
    #             "cy": 638.5824500671, "k1": 0.1789286566, "k2": 7.2702166765,
    #             "p1": -0.0000468215, "p2": -0.0003119220, "k3": 1.0951213863,
    #             "k4": 0.5601386744, "k5": 7.3133322005, "k6": 3.7433992330},
    #     1 : {"fx": 979.6145878730, "fy": 979.5805359372, "cx": 959.3375221475,
    #             "cy": 637.4537078957, "k1": 1.0563212267, "k2": 0.1334186749,
    #             "p1": -0.0000773611, "p2": 0.0000094945, "k3": -0.0004692985,
    #             "k4": 1.4543792145, "k5": 0.4278107646, "k6": 0.0092050339},
    #     2 : {"fx": 974.3228755212, "fy": 972.7458452371, "cx": 968.3878840220,
    #             "cy": 633.6952024248, "k1": 1.5156654373, "k2": 2.0003653250,
    #             "p1": -0.0000916370, "p2": -0.0005971661, "k3": 0.2228216789,
    #             "k4": 1.9050820620, "k5": 2.5090655303, "k6": 0.8483226282},
    #     3 : {"fx": 980.9329077772, "fy": 980.6324457616, "cx": 970.5813289162,
    #             "cy": 632.5460365801, "k1": -0.1151136546, "k2": -0.4224477115,
    #             "p1": 0.0000972238, "p2": -0.0000932816, "k3": -0.0197204029,
    #             "k4": 0.2789752545, "k5": -0.5768819225, "k6": -0.1171662892}
    # }
    '''saic,4月25收到的，2月份数据去畸变内参'''
    intrin_dict = {
        0 : {"fx": 980.3800193514499597, "fy": 980.7782165202912665, "cx": 955.5322522525138993,
            "cy": 635.2716285579763280, "k1": 0.9882385716789389152, "k2":  0.09428266084042861983,
            "p1": 0.0001111181413773584716, "p2": 0.0000141819422366783, "k3": -0.00253015557288906,
            "k4": 1.38626595670354, "k5": 0.363636977630938, "k6": -0.00160428030126683},
        1 : {"fx": 980.50541963903, "fy": 980.431929638899, "cx": 964.958625417331,
            "cy": 634.3540893399, "k1": 0.558440583029984, "k2": 0.127382513878998,
            "p1": 0.000199492234173769, "p2": 0.0000609043405864983, "k3": 0.00731234669561798,
            "k4": 0.940570020802693, "k5": 0.253714706868336, "k6": 0.036140837421252},
        2 : {"fx": 979.957641962313, "fy": 980.008662809892, "cx": 953.064550458191,
            "cy": 640.271891297242, "k1": 4.37865664254535, "k2": 1.69672052228799,
            "p1": 0.000018370374630882, "p2": 0.0000723994332536708, "k3": 0.0472160739259814,
            "k4": 4.77760256246426, "k5": 3.29901687941982, "k6": 0.343016980587562},
        3 : {"fx": 980.410462182264, "fy": 980.682567239638, "cx": 952.243940898891,
            "cy": 633.936725535851, "k1": 0.222492338231556, "k2": -0.0879090531527576,
            "p1": 0.000873256112812557, "p2": 0.000652281329874995, "k3": -0.00250717001953266,
            "k4": 0.609830939223342, "k5": -0.0958413970509091, "k6": -0.0199787674593401}    
    }


    import os
    image_list = []
    for root, dirs, files in os.walk(data_root):
        for ff in files:
            # print(root, dirs, ff)
            # if "image" in root:
            if "SideFrontLeft" in root:
                camera_index = 0   
            elif "SideFrontRight" in root:
                camera_index = 1
            elif "SideRearLeft" in root:
                camera_index = 2
            elif "SideRearRight" in root:
                camera_index = 3
            image_path = os.path.join(root, ff)
            print(image_path)
            orig_image = cv2.imread(image_path)
            undist_image, new_camera_intrin = undist_cvundistort(orig_image, intrin_dict[camera_index])
            # cv2.imshow("image", undist_image)
            dstpath = os.path.join(dst,ff)
            cv2.imwrite(dstpath, undist_image)

