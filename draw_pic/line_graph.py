#coding:utf-8
import matplotlib.pyplot as plt


'''
召回率
'''
def draw_recall():
    x = ['car','truck','bus','pedestrian','bicycle','motorcycle','tricycle']
    y1_cust_request_recall = [94,93.2,93.3,91.9,91.7,92.2,95.5]
    y2_perce_day_recall = [98.8,97.5,96.8,92.6,97.7,97.6,98.8]
    y3_perce_night_recall = [98.5,88,98.1,89,93.8,96.4,100]

    plt.title('recall compare between lable and perce')
    plt.plot(x, y1_cust_request_recall, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
    plt.plot(x, y2_perce_day_recall, marker='o', markersize=3)
    plt.plot(x, y3_perce_night_recall, marker='o', markersize=3)

    for a, b in zip(x, y1_cust_request_recall):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
    for a, b in zip(x, y2_perce_day_recall):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(x, y3_perce_night_recall):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=10)

    plt.legend(['cust_request_recall', 'perce_day_recall', 'perce_night_recall'])  # 设置折线名称
    plt.show()  # 显示折线图


'''
精确率
'''
def draw_precision():
    x = ['car','truck','bus','pedestrian','bicycle','motorcycle','tricycle']
    y1_lable_precision = [88.3,89.1,90.3,87.2,86.9,90.3,87.9]
    y2_perce_day_precision = [98.4,93.2,95.3,86.7,72.8,94.5,81.2]
    y3_perce_night_precision = [98,85,98.1,82.4,37.5,93,68.3]

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

    plt.legend(['cust_request_precision', 'perce_day_precision', 'perce_night_precision'])  # 设置折线名称
    plt.show()  # 显示折线图


def main():
    draw_recall()
    draw_precision()


if __name__=='__main__':
    main()