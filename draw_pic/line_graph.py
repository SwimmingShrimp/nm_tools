#coding:utf-8
import matplotlib.pyplot as plt


'''
召回率
'''
# x = ['car','truck','bus','pedestrian','bicycle','motorcycle','tricycle']
# y1_lable_recall = [94,93.2,93.3,91.9,91.7,92.2,95.5]
# y2_perce_day_recall = [99.5,99.4,98.6,93.6,98.9,99,99.1]
# y3_perce_night_recall = [98.6,93.8,100,85.5,94.1,98.8,100]

# plt.title('recall compare between lable and perce')
# plt.plot(x, y1_lable_recall, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
# plt.plot(x, y2_perce_day_recall, marker='o', markersize=3)
# plt.plot(x, y3_perce_night_recall, marker='o', markersize=3)

# for a, b in zip(x, y1_lable_recall):
#     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
# for a, b in zip(x, y2_perce_day_recall):
#     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
# for a, b in zip(x, y3_perce_night_recall):
#     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

# plt.legend(['lable_recall', 'perce_day_recall', 'perce_night_recall'])  # 设置折线名称
# plt.show()  # 显示折线图


'''
精确率
'''
x = ['car','truck','bus','pedestrian','bicycle','motorcycle','tricycle']
y1_lable_precision = [88.3,89.1,90.3,87.2,86.9,90.3,87.9]
y2_perce_day_precision = [99,91.2,97,88.6,69.5,95.9,80.3]
y3_perce_night_precision = [98,86.9,96.3,80.4,35.2,95.4,65.9]

plt.title('precision compare between lable and perce')
plt.plot(x, y1_lable_precision, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
plt.plot(x, y2_perce_day_precision, marker='o', markersize=3)
plt.plot(x, y3_perce_night_precision, marker='o', markersize=3)

for a, b in zip(x, y1_lable_precision):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
for a, b in zip(x, y2_perce_day_precision):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(x, y3_perce_night_precision):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

plt.legend(['lable_precision', 'perce_day_precision', 'perce_night_precision'])  # 设置折线名称
plt.show()  # 显示折线图