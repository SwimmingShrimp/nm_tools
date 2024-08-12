'''
Author: lixialin lixialin@nullmax.ai
Date: 2024-06-11 16:44:18
LastEditors: lixialin lixialin@nullmax.ai
LastEditTime: 2024-06-16 20:03:11
'''
import math
import numpy as np
import pandas as pd
import sys
import os

def two_points_2_straight_line(p1,p2):
    # 直线的一般方程可以表示为 Ax+By+C=0，其中 A、B 和 C 是常数
    x1,y1 = p1
    x2,y2 = p2
    if x2 != x1:
        m = (y2-y1)/(x2-x1)
        L1_A1 = -m
        L1_B1 = 1
        L1_C1 = m * x1 - y1
    else:
        L1_A1 = 1
        L1_B1 = 0
        L1_C1 = -x1
        return L1_A1, L1_B1, L1_C1
    # print(f"根据垂直点和测量点，计算出经过这两点的直线：L1_A1={L1_A1},L1_B1={L1_B1},C={L1_C1}")
    return round(L1_A1,3), round(L1_B1,3), round(L1_C1,3)

def pass_one_point_parallel_straight_line(p3,L1_A1,L1_B1,L1_C1):
    # 2条线平行，所以只有C发生变化
    x3,y3 = p3
    m = -L1_A1/L1_B1 if L1_B1 != 0 else float('inf')
    L2_C2 = x3*m - y3
    # print(f"经过预测点跟测量直线平行的直线：L2_A2={L1_A1},L2_B2={L1_B1},L2_C2={L2_C2}")
    return round(L2_C2,3)   

def pass_one_point_perpendicular_straight_line_distance(L2_A2,L2_B2,L2_C2):
    # 经过的点为后轴中心点
    # 2条线垂直，斜率发生变化，-1/m；
    m = -L2_A2 / L2_B2 if L2_B2 != 0 else 0
    if m == 0 :
        # 原直线垂直于x轴，新直线垂直于y轴
        m_perpendicular = 0
    else:
        m_perpendicular = -1 / m

    L3_A3 = L2_B2 if m_perpendicular != 0 else 1  # 斜率不为0时，A = B，否则新直线垂直于y轴
    L3_B3 = -L2_A2 if m_perpendicular != 0 else 0  # 斜率不为0时，B = -A
    # C = A*x1 - B*y1，因为经过的是后轴中心点，即原点，所以C为0
    L3_C3 = 0
    # print(f"经过原点，垂直于预测点直线的直线：L3_A3={L3_A3},L3_B3={L3_B3},L3_C3={L3_C3}")
    # 假设相交的点为x,y，y = -C/B - A/B * x
    L2_L3_inter_x = (L3_C3*L2_B2 - L2_C2*L3_B3)/(L2_A2*L3_B3 - L2_B2*L3_A3)
    L2_L3_inter_y = -(L2_C2-L2_A2*L2_L3_inter_x)/L2_B2
    # print(f"经过后轴中心点，预测点直线和垂线的角点坐标：({x},{y})")
    dist = (math.sqrt(L2_L3_inter_x**2 + L2_L3_inter_y**2))*100
    # print(f"后轴中心点到预测点垂线的距离={dist}")
    return round(L3_A3,3),round(L3_B3,3),round(L3_C3,3),round(L2_L3_inter_x,3),round(L2_L3_inter_y,3),round(dist,3)

def get_2points_depend_gt_p(L1_p1,measure_gt_dist):
    x1,y1 = L1_p1
    if x1==0:
        if measure_gt_dist >= abs(y1):
            sys.exit('数据有误，请检查！')
        else:
            l = math.sqrt(y1**2 - measure_gt_dist**2)
            L1_x2 = -(l*measure_gt_dist/abs(y1))
            L1_y2 = -(measure_gt_dist*measure_gt_dist/abs(y1))
    elif y1==0:
        if measure_gt_dist >= abs(x1):
            sys.exit('数据有误，请检查！')
        else:
            l = math.sqrt(x1**2 - measure_gt_dist**2)
            print(f"l={l}")
            L1_x2 = -(measure_gt_dist*measure_gt_dist/abs(x1))
            L1_y2 = -(l*measure_gt_dist/abs(x1))
    elif x1!=0 and y1!=0:
        L1_x2 = 2
        L1_y2 = y1
    # print(f"根据点和垂直距离，计算出垂直点的坐标：(x2,y2)=({x2},{y2})")
    return L1_x2,L1_y2

def get_distance(L1_p1,measure_gt_dist,peception_point_list,test_type,point_num):
    # 根据测量的垂直距离和一个点，计算L1上的另外一个点
    L1_x2,L1_y2 = get_2points_depend_gt_p(L1_p1,measure_gt_dist)
    # 2个点确定一条直线，根据L1上的两个点计算出L1直线表达式
    L1_A1,L1_B1,L1_C1 = two_points_2_straight_line(L1_p1,(L1_x2,L1_y2))
    all_data = []
    for point in peception_point_list:
        # 跟直线L1平行，且经过p3点的直线L2
        L2_C2 = pass_one_point_parallel_straight_line(point,L1_A1,L1_B1,L1_C1)
        # 跟直线L2垂直，且经过后轴中线点的直线L3，输出L3的直线表达式、跟L2交叉点的坐标、后轴中心点到交叉点的距离
        L3_A3,L3_B3,L3_C3,L2_L3_inter_x,L2_L3_inter_y,dist = pass_one_point_perpendicular_straight_line_distance(L1_A1,L1_B1,L2_C2)
        all_data.append([test_type,point_num,L1_A1,L1_B1,L1_C1,L2_C2,L3_A3,L3_B3,L3_C3,(L1_x2,L1_y2),(L2_L3_inter_x,L2_L3_inter_y),point,measure_gt_dist,dist,measure_gt_dist-dist])
    return all_data
           

def analysis_data(save_path):
    deal_column_name = 'diff_dist'
    df['Group'] = df[deal_column_name].apply(lambda x: 'Positive' if x > 0 else 'Negative')
    '''每一把每一个点统计一次'''
    # 大于0的值进行数据统计
    stats_positive = df[df['Group'] == 'Positive'].groupby(["test_type","point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    wall_point_stats_positive = df[(df['Group'] == 'Positive') & (df['test_type'].str.contains('wall'))].groupby(["point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    roadedge_point_stats_positive = df[(df['Group'] == 'Positive') & (df['test_type'].str.contains('roadedge'))].groupby(["point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    type_stats_positive = df[df['Group'] == 'Positive'].groupby(["test_type"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    # 小于0的值进行数据统计
    stats_negative = df[df['Group'] == 'Negative'].groupby(["test_type","point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    wall_point_stats_negative = df[(df['Group'] == 'Negative') & (df['test_type'].str.contains('wall'))].groupby(["point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    point_stats_negative = df[(df['Group'] == 'Negative') & (df['test_type'].str.contains('roadedge'))].groupby(["point_num"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    type_stats_negative = df[df['Group'] == 'Negative'].groupby(["test_type"])[deal_column_name].agg(['min', 'max', 'mean', 'std'])
    # 所有数据进行数据统计
    df[deal_column_name] = df[deal_column_name].abs()
    stats_abs_all = df.groupby(["test_type","point_num"]).agg(['min', 'max', 'mean', 'std'])
    wall_point_stats_abs_all = df[df['test_type'].str.contains('wall')].groupby(["point_num"]).agg(['min', 'max', 'mean', 'std'])
    roadedge_point_stats_abs_all = df[df['test_type'].str.contains('roadedge')].groupby(["point_num"]).agg(['min', 'max', 'mean', 'std'])
    type_stats_abs_all = df.groupby(["test_type"]).agg(['min', 'max', 'mean', 'std'])
    with pd.ExcelWriter(save_path,mode='a',engine='openpyxl') as writer:
        stats_positive.to_excel(writer,sheet_name="靠近自车_每一把每个点位")
        wall_point_stats_positive.to_excel(writer,sheet_name="靠近自车_墙_相同点位")
        roadedge_point_stats_positive.to_excel(writer,sheet_name="靠近自车_路沿_相同点位")
        type_stats_positive.to_excel(writer,sheet_name="靠近自车_每一把所有点位")
        stats_negative.to_excel(writer,sheet_name="远离自车_每一把每个点位")
        wall_point_stats_negative.to_excel(writer,sheet_name="远离自车_墙_相同点位")
        point_stats_negative.to_excel(writer,sheet_name="远离自车_路沿_相同点位")
        type_stats_negative.to_excel(writer,sheet_name="远离自车_每一把所有点位")
        stats_abs_all.to_excel(writer,sheet_name="每一把每个点位")
        wall_point_stats_abs_all.to_excel(writer,sheet_name="墙_相同点位")
        roadedge_point_stats_abs_all.to_excel(writer,sheet_name="路沿_相同点位")
        type_stats_abs_all.to_excel(writer,sheet_name="每一把所有点位")



    



if __name__ ==  "__main__":
    # start_time|end_time|L1_x1|L1_y1|measure_gt_dist|test_type|point_num
    # (L1_x1,L1_y1)：是x轴或者y轴与路沿或者墙壁的交叉点，p_list：是感知输出的路沿或墙壁的点
    test_excel = '/home/ubuntu/Pictures/freespace_test.xlsx'
    save_path = '{}/{}.xlsx'.format('/home/ubuntu/Videos','result')

    # df = pd.read_excel(test_excel,skiprows=[1])
    # 从填写的excel中获取
    L1_p1 = (0,5)
    measure_gt_dist = 4
    test_type = 'roadedge3'
    point_num = 3
    # starttime = 
    # endtime =
    # 传入starttime和endtime，从rosbag中获取感知所有点的list
    peception_point_list = [(-2,-3),(-1,-5),(-4,-3)]

    # 根据以上信息，计算后轴中心点到感知检测点的垂直距离
    all_data = get_distance(L1_p1,measure_gt_dist,peception_point_list,test_type,point_num)
    all_data = []
    # for df_ in df:
    #     all_data_ = get_distance(L1_p1,measure_gt_dist,peception_point_list,test_type,point_num)
    #     all_data += all_data_
    columns_name = ["test_type","point_num","L1_A1","L1_B1","L1_C1","L2_C2","L3_A3","L3_B3","L3_C3","L1_compute_point","L2_L3_intersection_point","perception_point","measure_gt_dist","perception_dist","diff_dist",]
    df = pd.DataFrame(all_data, columns=columns_name)
    if not os.path.exists(save_path):
        df.to_excel(save_path,sheet_name=test_type)
    else:      
        with pd.ExcelWriter(save_path,mode='a',engine='openpyxl') as writer:
            df.to_excel(writer,sheet_name=test_type) 
    # 根据不同测试类型和点位进行分组分析，max,min,std,mean


