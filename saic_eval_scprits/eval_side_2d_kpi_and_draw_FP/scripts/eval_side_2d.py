#!/usr/bin/python
# -*- coding: utf-8 -*-
from ctypes import c_void_p
import pandas as pd
import argparse
from config.cfg import Config
import utils
import os
import cv2

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('lablepath', type=str, help='标注文件路径')
    parser.add_argument('percepath', type=str, help='感知文件路径')
    parser.add_argument('pic_path', type=str, help='图片路径')
    parser.add_argument('save_FN_path', type=str, help='FN图片保存文件夹路径')
    parser.add_argument('save_FP_path', type=str, help='FP图片保存文件夹路径')
    args = parser.parse_args()
    return args

@utils.register('环视-recall', 'KPI')

def get_recall_side(label_jsons, perce_jsons):
    '''召回率获取'''
    if not label_jsons or len(label_jsons) != 1 or not perce_jsons[0].endswith('.json'):
        print('无2d检测标注数据')
        return
    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    df = pd.DataFrame(columns=['KPI']+ analyze_obstacle_type+ ['other'])
    row = df.shape[0]
    df.loc[row + 0, 'KPI'] = '标注数量'
    df.loc[row + 1, 'KPI'] = '检出正确'
    df.loc[row + 2, 'KPI'] = '检出错误'
    df.loc[row + 3, 'KPI'] = '召回率'
    df.fillna(0, inplace=True)

    for label_result, perce_result,perce_json in utils.get_match_img_one_json(label_jsons, perce_jsons):    ###得到一张图片对应的json真值与感知结果
        if not label_result or not perce_result:    ###有的图片没有标注障碍物，直接跳过不进行评测
            continue

        ###根据perce_json的路径信息得到对应图片的路径
        dir_path = perce_json.rsplit('/', 2)[0]
        img_path = perce_json.replace('.json', '.png').replace(dir_path, pic_path)
        print(img_path)

        for label_data, perce_data in utils.get_match_obstacle_recall_side(label_result, perce_result,img_path,FN_path):        ###得到障碍物的json真值与感知数据结果
            if not label_data:
                continue
            label_type = label_data['tags']["class"]
            perce_type = None if not perce_data else enum_obstacle_type[perce_data["obstacle_type"]]
            result_type = label_type if label_type in analyze_obstacle_type else 'other'

            df.iloc[row + 0, df.columns.get_loc(result_type)] += 1
            if perce_type and perce_type == label_type:
                df.iloc[row + 1, df.columns.get_loc(result_type)] += 1
            elif perce_type:
                df.iloc[row + 2, df.columns.get_loc(result_type)] += 1



    df['all_type'] = df.iloc[:, 1:-2].apply(lambda x: x.sum(), axis=1)
    df.iloc[row + 3, 1:] = df.iloc[:, 1:].apply(
        lambda x: 0 if not x[0] else "%.1f" % (100 * (x[1] + x[2]) / float(x[0])))

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(df)

@utils.register('环视-precision', 'KPI')
def get_precision_side(label_jsons, perce_jsons):
    '''精确率获取'''
    if not label_jsons or len(label_jsons) != 1 or not perce_jsons[0].endswith('.json'):
        print('无2d检测标注数据')
        return
    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    df = pd.DataFrame(columns=['KPI'] + analyze_obstacle_type + ['other'])
    row = df.shape[0]
    df.loc[row + 0, 'KPI'] = '正确检出'
    df.loc[row + 1, 'KPI'] = '错误检出'
    df.loc[row + 2, 'KPI'] = '精确率'
    df.fillna(0, inplace=True)
    print(label_jsons,perce_jsons)
    for label_result, perce_result,perce_json in utils.get_match_img_one_json(label_jsons, perce_jsons):   ###得到一张图片对应的真值与感知结果
        if not perce_result:
            continue

        ###根据perce_json的路径信息得到对应图片的路径
        dir_path = perce_json.rsplit('/',2)[0]
        img_path = perce_json.replace('.json','.png').replace(dir_path,pic_path)


        for label_data, perce_data in utils.get_match_obstacle_precision_side(label_result, perce_result,img_path,FP_path):     ###得到障碍物的json真值与感知数据结果
            if not perce_data:
                continue
            perce_type = enum_obstacle_type[perce_data["obstacle_type"]]
            label_type = label_data['tags']["class"] if label_data else None
            result_type = perce_type if perce_type in analyze_obstacle_type else 'other'
            if perce_type == label_type:
                df.iloc[row + 0, df.columns.get_loc(result_type)] += 1
            elif perce_type:
                df.iloc[row + 1, df.columns.get_loc(result_type)] += 1
    df['all_type'] = df.iloc[:, 1:-2].apply(lambda x: x.sum(), axis=1)
    df.iloc[row + 2, 1:] = df.iloc[:, 1:].apply(lambda x: 0 if not x[0] else "%.1f" % (100 * x[0] / float(x[0] + x[1])))
    print(df)

if __name__ == '__main__':

    args = parse_args()
    lable_path = args.lablepath
    perce_path = args.percepath
    pic_path = args.pic_path
    FN_path = args.save_FN_path
    FP_path = args.save_FP_path

    perce_json_files = utils.get_all_files(perce_path, '.json')   #得到所有json文件路径的列表
    label_json_files = utils.get_all_files(lable_path, '.json')

    get_recall_side(label_json_files,perce_json_files)
    #get_precision_side(label_json_files, perce_json_files)

