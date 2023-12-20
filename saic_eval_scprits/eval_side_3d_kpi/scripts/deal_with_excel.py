import numpy as np
import pandas as pd

### 测距 kpi ###
def deal_with_dist():
    #读取表格数据
    df1 = pd.read_excel('./0803_case1_dist.xlsx')
    df2 = pd.read_excel('./0803_case2_dist.xlsx')

    #表格数据计算
    first_avg = (df1['first']*df1['first_count'] + df2['first']*df2['first_count']) / (df1['first_count']+df2['first_count'])
    second_avg = (df1['second']*df1['second_count'] + df2['second']*df2['second_count']) / (df1['second_count']+df2['second_count'])
    third_avg = (df1['third']*df1['third_count'] + df2['third']*df2['third_count']) / (df1['third_count']+df2['third_count'])
    Xrange_avg = (df1['Xrange']*df1['Xrange_count'] + df2['Xrange']*df2['Xrange_count']) / (df1['Xrange_count']+df2['Xrange_count'])

    #计算结果写入表格
    df2['first_avg'] = first_avg
    df2['second_avg'] = second_avg
    df2['third_avg'] = third_avg
    df2['Xrange_avg'] = Xrange_avg
    df2.fillna(0,inplace=True)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(df2)
    df2.to_excel('/home/songbing/Downloads/eval_side_3d_kpi/nullmax_vehicle/scripts/0803_case2_dist.xlsx')


### 测速 kpi ###
def deal_with_speed():
    #读取表格数据
    df1 = pd.read_excel('./0801_case1_speed.xlsx')
    df2 = pd.read_excel('./0801_case2_speed.xlsx')

    #表格数据计算
    velocity_x_avg = (df1['velocity_x']*df1['velocity_x_count'] + df2['velocity_x']*df2['velocity_x_count']) / (df1['velocity_x_count']+df2['velocity_x_count'])
    velocity_y_avg = (df1['velocity_y']*df1['velocity_y_count'] + df2['velocity_y']*df2['velocity_y_count']) / (df1['velocity_y_count']+df2['velocity_y_count'])

    #计算结果写入表格
    df2['velocity_x_avg'] = velocity_x_avg
    df2['velocity_y_avg'] = velocity_y_avg
    df2.fillna(0,inplace=True)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(df2)
    df2.to_excel('/home/songbing/Downloads/eval_side_3d_kpi/nullmax_vehicle/scripts/0801_case2_speed.xlsx')


### 测长宽高 kpi ###
def deal_with_dimension():
    #读取表格数据
    df1 = pd.read_excel('./0730_case1_dimension.xlsx')
    df2 = pd.read_excel('./0730_case2_dimension.xlsx')

    #表格数据计算
    Length_avg = (df1['Length']*df1['Count']+df2['Length']*df2['Count']) / (df1['Count']+df2['Count'])
    Width_avg = (df1['Width']*df1['Count']+df2['Width']*df2['Count']) / (df1['Count']+df2['Count'])
    Height_avg = (df1['Height']*df1['Count']+df2['Height']*df2['Count']) / (df1['Count']+df2['Count'])

    #计算结果写入表格
    df2['Length_avg'] = Length_avg
    df2['Width_avg'] = Width_avg
    df2['Height_avg'] = Height_avg
    df2.fillna(0,inplace=True)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(df2)
    df2.to_excel('/home/songbing/Downloads/eval_side_3d_kpi/nullmax_vehicle/scripts/0730_case2_dimension.xlsx')


### 测yaw kpi ###
def deal_with_yaw():
    #读取表格数据
    df1 = pd.read_excel('./0730_case1_yaw.xlsx')
    df2 = pd.read_excel('./0730_case2_yaw.xlsx')

    #表格数据计算
    yaw_avg = (df1['yaw']*df1['Count']+df2['yaw']*df2['Count']) / (df1['Count']+df2['Count'])

    df2['yaw_avg'] = yaw_avg
    df2.fillna(0,inplace=True)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(df2)
    df2.to_excel('/home/songbing/Downloads/eval_side_3d_kpi/nullmax_vehicle/scripts/0730_case2_yaw.xlsx')

if __name__ == '__main__':
    deal_with_dist()
    #deal_with_speed()
    #deal_with_dimension()
    #deal_with_yaw()