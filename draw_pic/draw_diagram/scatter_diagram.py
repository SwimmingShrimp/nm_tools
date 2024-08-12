import matplotlib.pyplot as plt
import os


save_path = '/home/ubuntu/Videos'
test_type ="wall1"
point_num = 1
title = test_type + '_' + str(point_num)


# 假设我们有一些数据点
x = [1, 2, 3, 4, 5]  # x轴坐标
y = [2, 3, 5, 7, 11] # y轴坐标

plt.scatter(x,y)
plt.title(title)
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
# plt.show()
plt.savefig(os.path.join(save_path,title + '.jpg'))




