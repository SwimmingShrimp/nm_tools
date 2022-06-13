import os
import pandas as pd

df = pd.DataFrame(['car', 'truck', 'bus', 'tricycle', 'motorcycle', 'bicycle', 'pedestrian'])
df.fillna(0, inplace=True)
txt_src = 'C:/Users/李夏临/Desktop/front_3d/1.txt'
with open(txt_src,'r',encoding='utf-8') as f:
    lines = f.readlines()
    idx = 1
    for line in lines:
        line_list = line.split(',')
        if len(line_list)<2:
            continue
        print(line_list)        
        df.loc[idx, 'car']= line_list[1]
        df.loc[idx, 'truck']= line_list[2]
        df.loc[idx, 'bus']= line_list[3]
        df.loc[idx, 'tricycle']= line_list[4]
        df.loc[idx, 'motorcycle']= line_list[5]
        df.loc[idx, 'bicycle']= line_list[6]
        df.loc[idx, 'pedestrian']= line_list[7]
        idx+=1
        df.to_excel('C:/Users/李夏临/Desktop/front_3d/1.xlsx')
