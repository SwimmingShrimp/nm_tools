import os
import cv2
import pcl
import numpy as np
import pcl.pcl_visualization
import random
from tqdm import tqdm
#30
T_lc = np.array([[-0.00677942, -0.99997666, 0.00085239, 0.0400204 ], 
                  [ 0.00681351, -0.00089858, -0.99997638, -0.42483596], 
                  [ 0.99995381, -0.00677345, 0.00681944, -0.38988517], 
                  [ 0. , 0. , 0. , 1. ]])
K = np.array([[3937.2814445759755/3. ,    0.       ,  988.87655530274765/3.],
               [   0.       , 3938.8568711591438/3. ,  506.11922601688411/3.],
               [   0.       ,    0.       ,    1.       ]])
#120
#T_lc = np.array([[ 0.01238735, -0.99991702,  0.00353619, -0.01350114],
#                 [ 0.02203001, -0.00326269, -0.99975199, -0.432903  ],
#                 [ 0.99968057,  0.01246218,  0.02198776, -0.39810411],
#                 [ 0.,          0.,          0.,          1.        ]])
#K = np.array([[964.2857143/3 ,    0.         ,  963.0385105/3],
#              [   0.         , 964.2857143/3 ,  504.0914833/3],
#              [   0.         ,     0.        ,    1.       ]])

ts_path = '/media/jiaoyufei/planning1/1102/config/timestamp_vc2.log'
ts_dict = dict()
with open(ts_path, 'r') as f:
    lines = f.readlines()

for line in lines:
    line = line.strip().split(' ')
    time = int(line[5])
    frameid = int(line[-1])
    ts_dict[frameid] = 	time
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 360
save_dir = './depth/30/frame_vc2_{}.bmp'

with open('/data1/NMtest/others/DataChoice/NullMax/3D/pcd.txt', 'r') as f:
    lines = f.readlines()
#lines = random.sample(lines, 100)
for line in tqdm(lines):
    pcd_path = line.strip()
    pcd_time = pcd_path.split('.pcd')[0].split('/')[-1]
    it, fl = pcd_time.split('.')
    it = int(it)
    pcd_time = it*1000000 + int(int(fl)/1000)
    pcd_time = pcd_time + 400000

    mindiff = 100000.
    finalid = -1
    for k, v in ts_dict.items():
        diff = abs(v - pcd_time)
        if diff < mindiff:
            mindiff = diff
            finalid = k
    cloud = pcl.load(pcd_path)
    points_L=[]

    for i in range(0, cloud.size):
        x = cloud[i][0]
        y = cloud[i][1]
        z = cloud[i][2]
        if x == x:
            points_L.append([x,y,z,1])
    points_L = np.array(points_L, ndmin=2).astype(np.float32)
    points_C = np.matmul(T_lc, points_L.T)[:3, :]
    points_uv = np.matmul(K, points_C)[:2]
    points_z = points_C[2]
    points_uv = (points_uv / points_z).round().astype(int)
    mask = (points_uv[0, :] >=0) &\
                (points_uv[0, :] < IMAGE_WIDTH) &\
                (points_uv[1, :] >=0) &\
                (points_uv[1, :] < IMAGE_HEIGHT)
    points_uv_valid = points_uv[:, mask]
    points_z_valid = points_z[mask]
    depth_img = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH)) 
    depth_img[points_uv_valid[1], points_uv_valid[0]] = points_z_valid
    pad_depth = np.zeros((384, 640))
    pad_depth[12:372, :] = depth_img
    cv2.imwrite(save_dir.format(finalid), pad_depth)



