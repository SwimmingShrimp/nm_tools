import argparse
import os
from glob import glob
import numpy as np
import cv2


if __name__ == '__main__':
    img_path = '/home/pengjianlin/nullmax/libcbdetect/waimian/fish_right.png'
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    # import pdb;pdb.set_trace()
    camera_matrix = np.array([[316.666, 0, 640],
                              [0, 316.666, 480],
                              [0, 0, 1]])
    dist_coefs = np.array([0.129777, -0.0299406, 0.00785671, -0.00174837])
    # camera_matrix = np.array([[511.0273541887217, 0, 928.2615607387517],
    #                           [0, 510.83972965082967, 550.983448857282],
    #                           [0, 0, 1]])
    # dist_coefs = np.array([0.12965710302674566, -0.027275970838676764, -0.00029428038050454856, -0.004998151885110799])
    newcameramtx = np.array([[200.0, 0, 640],
                              [0, 200.0, 480],
                              [0, 0, 1]])
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 1.5, (w, h))
    # import pdb;pdb.set_trace()
    undistort_maps = cv2.fisheye.initUndistortRectifyMap(camera_matrix, dist_coefs, np.eye(3), newcameramtx, (w, h), cv2.CV_16SC2)
    result = cv2.remap(img, *undistort_maps, interpolation=cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_CONSTANT)
    # import pdb;pdb.set_trace()
    # cv2.imwrite(os.path.join('calibrate_result', 'calibrate_' + img_path.split('/')[-1]), result)
    cv2.imwrite('/home/pengjianlin/nullmax/libcbdetect/waimian/fish_right_dist.png', result)
    cv2.imshow('123', result)
    cv2.waitKey(0)