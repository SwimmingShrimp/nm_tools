# coding=utf-8
import json
import os

def get_json_data(json_file):
    with open(json_file) as f:
        json_data = json.load(f)
        return json_data

src = '/home/NULLMAX/lixialin/音乐/20220316/new/'
src1 = src + 'side_left_front.json'
src2 = src + 'side_left_rear.json'
src3 = src + 'side_right_front.json'
src4 = src + 'side_right_rear.json'
dst = src + 'day.json'

json_data = []
json_data1 = get_json_data(src1)
json_data2 = get_json_data(src2)
json_data3 = get_json_data(src3)
json_data4 = get_json_data(src4)
json_data = json_data1+json_data2 +json_data3 +json_data4

with open(dst,'w') as f:
    json.dump(json_data, f, indent=4)


