from sklearn.linear_model import LinearRegression,RANSACRegressor
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import time

def filter_outiers(points):
    # 全量数据画图
    # x = [x for x,y in points]
    # y = [y for x,y in points]
    # plt.plot(x,y,'o',label='all_data')
    # plt.legend(loc='upper left')
    # plt.show()

    x = np.array([[x] for x,y in points])
    y = np.array([y for x,y in points])
    model_ransac = RANSACRegressor(LinearRegression(),min_samples=200,max_trials=100,residual_threshold=0.18)    # 使用RANSAC算法
    model_ransac.fit(x,y)
    inlier_mask = model_ransac.inlier_mask_
    outlier_mask = np.logical_not(inlier_mask)
    line_X = np.arange(-10, 10)
    line_y_ransac = model_ransac.predict(line_X[:, np.newaxis])
    len_inliner = len(x[inlier_mask])
    len_outliner = len(x[outlier_mask])
    print(f"outliner_num = {len_outliner}, inlier_num = {len_inliner}")
    plt.plot(x[inlier_mask], y[inlier_mask], '.g', label='Inliers')
    plt.plot(x[outlier_mask], y[outlier_mask], '.r', label='Outliers')
    plt.plot(line_X, line_y_ransac, '-b', label="RANSAC Regression")
    plt.legend(loc='upper left')
    plt.show()

points =[]
filter_outiers(points)