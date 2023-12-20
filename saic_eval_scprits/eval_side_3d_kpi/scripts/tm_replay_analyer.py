#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
from hashlib import md5
import json
import shutil
import tqdm
import pandas as pd
import math
from config.cfg import Config
import utils
import os
import datetime
import argparse


def get_replay_result(label_jsons, perce_jsons, func_list):
    file_name = utils.BASIC_NAME + "KPI" + '.xlsx'
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 500)
    for func in func_list:
        eval(func)(label_jsons, perce_jsons, file_name)


def get_recall_side(label_jsons, perce_jsons, file_name):
    '''召回率获取'''
    if not label_jsons or len(label_jsons) != 1 or not perce_jsons[0].endswith('.json'):
        print('无2d检测标注数据')
        return
    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    df = pd.DataFrame(columns=['KPI'] + analyze_obstacle_type + ['other'])
    row = df.shape[0]
    df.loc[row + 0, 'KPI'] = '标注数量'
    df.loc[row + 1, 'KPI'] = '检出正确'
    df.loc[row + 2, 'KPI'] = '检出错误'
    df.loc[row + 3, 'KPI'] = '召回率'
    df.fillna(0, inplace=True)

    for label_result, perce_result in utils.get_match_img_one_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_recall_side(label_result, perce_result):
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
    print(df)
    utils.write_to_excel(df=df, file_name=file_name, sheet_name='type')


def get_precision_side(label_jsons, perce_jsons, file_name):
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

    for label_result, perce_result in utils.get_match_img_one_json(label_jsons, perce_jsons):
        if not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_precision_side(label_result, perce_result):
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
    # utils.write_to_excel(df=df, file_name=file_name, sheet_name='type')

def get_ranging_side(label_jsons, perce_jsons, file_name):
    '''测距效果获取'''
    if not label_jsons or len(label_jsons) <= 1 or not perce_jsons[0].endswith('.json'):
        print('无3d检测标注数据')
        return

    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]

    enum_obstacle_x, enum_obstacle_y = configs["ranging_obstacle_x"], configs["ranging_obstacle_y"]
    columns = ['obstacle', 'Dx'] + sorted(list(enum_obstacle_y.keys())) + sorted(
        [x + '_count' for x in enum_obstacle_y.keys()])
    index = ['_'.join([x, y]) for x in analyze_obstacle_type for y in sorted(enum_obstacle_x.keys())]

    df = pd.DataFrame(columns=columns, index=index)
    df['obstacle'] = [x.split('_')[0] for x in index]
    df['Dx'] = [x.split('_')[1] for x in index]
    df.fillna(0, inplace=True)

    for label_result, perce_result, fusion_result in utils.get_match_img_more_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_3d(label_result, perce_result, fusion_result):

            label_type = enum_obstacle_type[label_data['type']]
            label_position_x = label_data['box_3d']["global_dists"]['x']
            label_position_y = label_data['box_3d']["global_dists"]['y']

            if abs(label_position_x) > 60 or abs(label_position_y) > 15:
                continue

            perce_position_x = perce_data["position"]['obstacle_pos_x_filter']
            perce_position_y = perce_data["position"]['obstacle_pos_y_filter']

            distance_tolerance_x_percent = abs((perce_position_x - label_position_x) / label_position_x)
            distance_tolerance_y_percent = abs((perce_position_y - label_position_y) / label_position_y)

            if abs(label_position_x) < 20:
                if distance_tolerance_y_percent > 0.2:
                    print("label_position_y is {}".format(label_position_y))
                    print("perce_position_y is {}".format(perce_position_y))
                    print("distance_tolerance_y_percent is {}".format(distance_tolerance_y_percent))

            # if distance_tolerance_x_percent > 5:
            #     print("label_position_x is {}".format(label_position_x))
            #     print("perce_position_x is {}".format(perce_position_x))
            #     print("distance_tolerance_x_percent is {}".format(distance_tolerance_x_percent))

            result_type = label_type if label_type in analyze_obstacle_type else 'other'

            for index_key, threshold_x in enum_obstacle_x.items():
                if not threshold_x[0] < abs(label_position_x) <= threshold_x[1] or result_type == 'other':
                    continue
                for columns_key, threshold_y in enum_obstacle_y.items():
                    if threshold_y[0] < abs(label_position_y) <= threshold_y[1] and columns_key != 'Xrange':
                        index_name = "_".join([result_type, index_key])
                        df.loc[index_name, columns_key] += distance_tolerance_y_percent
                        df.loc[index_name, columns_key + '_count'] += 1
                    elif threshold_y[0] < abs(label_position_y) <= threshold_y[1] and columns_key == 'Xrange':
                        index_name = "_".join([result_type, index_key])
                        df.loc[index_name, columns_key] += distance_tolerance_x_percent
                        df.loc[index_name, columns_key + '_count'] += 1

    for column_key in enum_obstacle_y.keys():
        df[column_key] = df[column_key] / df[column_key + '_count']
        df[column_key] = pd.to_numeric(df[column_key].apply(lambda x: '%.4f' % x), errors='coerce')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df.fillna(0, inplace=True)
    print(df)
    #utils.write_to_excel(df=df, file_name=file_name, sheet_name='distance')


@utils.register('环视-测速', 'KPI')
def get_velocity_side(label_jsons, perce_jsons, file_name):
    '''测速效果获取'''
    if not label_jsons or len(label_jsons) <= 1 or not perce_jsons[0].endswith('.json'):
        print('无3d检测标注数据')
        return

    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    enum_obstacle_x, enum_obstacle_y = configs["ranging_obstacle_x"], configs["ranging_obstacle_y"]
    columns = ['obstacle', 'Dx', 'velocity_x', 'velocity_y', 'velocity_x_count', 'velocity_y_count']
    index = ['_'.join([x, y]) for x in analyze_obstacle_type for y in sorted(enum_obstacle_x.keys())]

    df = pd.DataFrame(columns=columns, index=index)
    df['obstacle'] = [x.split('_')[0] for x in index]
    df['Dx'] = [x.split('_')[1] for x in index]
    df.fillna(0, inplace=True)

    for label_result, perce_result, fusion_result in utils.get_match_img_more_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_3d(label_result, perce_result, fusion_result):
            if not perce_data or perce_data['obstacle_valid'] == 0:
                continue
            label_type = enum_obstacle_type[label_data['type']]
            label_position_x = label_data['box_3d']["global_dists"]['x']
            label_velocity_x = label_data['box_3d']["velocity"]['x']
            label_velocity_y = label_data['box_3d']["velocity"]['y']

            if abs(label_velocity_x) > 300 or abs(label_velocity_y) > 300:
                continue

            if label_velocity_x == -1000:
                continue

            perce_velocity_x = perce_data["velocity"]['obstacle_rel_vel_x_filter']
            perce_velocity_y = perce_data["velocity"]['obstacle_rel_vel_y_filter']

            velocity_tolerance_x = abs(perce_velocity_x - label_velocity_x)
            velocity_tolerance_y = abs(perce_velocity_y - label_velocity_y)

            result_type = label_type if label_type in analyze_obstacle_type else 'other'
            for index_key, threshold_x in enum_obstacle_x.items():
                if threshold_x[0] < label_position_x <= threshold_x[1] and result_type != 'other':
                    index_name = "_".join([result_type, index_key])
                    df.loc[index_name, 'velocity_x'] += velocity_tolerance_x
                    df.loc[index_name, 'velocity_x_count'] += 1
                    index_name = "_".join([result_type, index_key])
                    df.loc[index_name, 'velocity_y'] += velocity_tolerance_y
                    df.loc[index_name, 'velocity_y_count'] += 1

    df['velocity_x'] = df['velocity_x'] / df['velocity_x_count']
    df['velocity_y'] = df['velocity_y'] / df['velocity_y_count']
    df['velocity_x'] = pd.to_numeric(df['velocity_x'].apply(lambda x: '%.2f' % x), errors='coerce')
    df['velocity_y'] = pd.to_numeric(df['velocity_y'].apply(lambda x: '%.2f' % x), errors='coerce')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df.fillna(0, inplace=True)
    utils.write_to_excel(df=df, file_name=file_name, sheet_name='velocity')


@utils.register('环视-测加速度', 'KPI')
def get_accel_side(label_jsons, perce_jsons, file_name):
    '''测加速度效果获取'''
    if not label_jsons or len(label_jsons) <= 1 or not perce_jsons[0].endswith('.json'):
        print('无3d检测标注数据')
        return

    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    enum_obstacle_x, enum_obstacle_y = configs["ranging_obstacle_x"], configs["ranging_obstacle_y"]
    columns = ['obstacle', 'Dx', 'accel_x', 'accel_y', 'accel_x_count', 'accel_y_count']
    index = ['_'.join([x, y]) for x in analyze_obstacle_type for y in sorted(enum_obstacle_x.keys())]

    df = pd.DataFrame(columns=columns, index=index)
    df['obstacle'] = [x.split('_')[0] for x in index]
    df['Dx'] = [x.split('_')[1] for x in index]
    df.fillna(0, inplace=True)

    for label_result, perce_result, fusion_result in utils.get_match_img_more_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_3d(label_result, perce_result, fusion_result):
            if not perce_data or perce_data['obstacle_valid'] == 0:
                continue
            label_type = enum_obstacle_type[label_data['type']]
            label_position_x = label_data['box_3d']["global_dists"]['x']

            label_accel_x = label_data['box_3d']["accel"]['x']
            label_accel_y = label_data['box_3d']["accel"]['y']

            if abs(label_accel_x) > 50 or abs(label_accel_y) > 50:
                continue

            if label_accel_x == -1000:
                continue

            perce_accel_x = perce_data["accel"]['obstacle_rel_acc_x_filter']
            perce_accel_y = perce_data["accel"]['obstacle_rel_acc_y_filter']

            accel_tolerance_x = abs(perce_accel_x - label_accel_x)
            accel_tolerance_y = abs(perce_accel_y - label_accel_y)

            result_type = label_type if label_type in analyze_obstacle_type else 'other'
            for index_key, threshold_x in enum_obstacle_x.items():
                if threshold_x[0] < label_position_x <= threshold_x[1] and result_type != 'other':
                    index_name = "_".join([result_type, index_key])
                    df.loc[index_name, 'accel_x'] += accel_tolerance_x
                    df.loc[index_name, 'accel_x_count'] += 1
                    index_name = "_".join([result_type, index_key])
                    df.loc[index_name, 'accel_y'] += accel_tolerance_y
                    df.loc[index_name, 'accel_y_count'] += 1
    df['accel_x'] = df['accel_x'] / df['accel_x_count']
    df['accel_y'] = df['accel_y'] / df['accel_y_count']
    df['accel_x'] = pd.to_numeric(df['accel_x'].apply(lambda x: '%.2f' % x), errors='coerce')
    df['accel_y'] = pd.to_numeric(df['accel_y'].apply(lambda x: '%.2f' % x), errors='coerce')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df.fillna(0, inplace=True)
    utils.write_to_excel(df=df, file_name=file_name, sheet_name='accel')


@utils.register('环视-测长宽高', 'KPI')
def get_dimension_side(label_jsons, perce_jsons, file_name):
    '''长宽高效果获取'''
    if not label_jsons or len(label_jsons) <= 1 or not perce_jsons[0].endswith('.json'):
        print('无3d检测标注数据')
        return

    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    columns = ['obstacle', 'Length', 'Width', 'Height', 'Count']
    index = [x for x in analyze_obstacle_type]

    df = pd.DataFrame(columns=columns, index=index)
    df['obstacle'] = [x for x in index]
    df.fillna(0, inplace=True)

    for label_result, perce_result, fusion_result in utils.get_match_img_more_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_3d(label_result, perce_result, fusion_result):
            if not perce_data or perce_data['obstacle_valid'] == 0:
                continue
            label_type = enum_obstacle_type[label_data['type']]

            # label_position_x = label_data['box_3d']["global_dists"]['x']
            # label_velocity_x = label_data['box_3d']["velocity"]['x']
            # label_velocity_y = label_data['box_3d']["velocity"]['y']

            label_length = label_data['dimension']['x']
            label_width = label_data['dimension']['y']
            label_height = label_data['dimension']['z']

            perce_length = perce_data["obstacle_length"]
            perce_width = perce_data["obstacle_width"]
            perce_height = perce_data["obstacle_height"]

            length_tolerance_percent = abs((perce_length - label_length) / label_length)
            width_tolerance_percent = abs((perce_width - label_width) / label_width)
            height_tolerance_percent = abs((perce_height - label_height) / label_height)

            if length_tolerance_percent > .5:
                print("label_length is {}".format(label_length))
                print("perce_length is {}".format(perce_length))
                print("length_tolerance_percent is {}".format(length_tolerance_percent))

            if width_tolerance_percent > .5:
                print("label_width is {}".format(label_width))
                print("perce_width is {}".format(perce_width))
                print("width_tolerance_percent is {}".format(width_tolerance_percent))

            if height_tolerance_percent > .5:
                print("label_height is {}".format(label_height))
                print("perce_height is {}".format(perce_height))
                print("height_tolerance_percent is {}".format(height_tolerance_percent))



            result_type = label_type if label_type in analyze_obstacle_type else 'other'

            # if result_type != 'other':
            index_name = result_type
            df.loc[index_name, 'Length'] += length_tolerance_percent
            df.loc[index_name, 'Width'] += width_tolerance_percent
            df.loc[index_name, 'Height'] += height_tolerance_percent
            df.loc[index_name, 'Count'] += 1

    df['Length'] = df['Length'] / df['Count']
    df['Width'] = df['Width'] / df['Count']
    df['Height'] = df['Height'] / df['Count']
    df['Length'] = pd.to_numeric(df['Length'].apply(lambda x: '%.4f' % x), errors='coerce')
    df['Width'] = pd.to_numeric(df['Width'].apply(lambda x: '%.4f' % x), errors='coerce')
    df['Height'] = pd.to_numeric(df['Height'].apply(lambda x: '%.4f' % x), errors='coerce')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df.fillna(0, inplace=True)
    utils.write_to_excel(df=df, file_name=file_name, sheet_name='dimension')


def get_yaw_side(label_jsons, perce_jsons, file_name):
    '''航向角效果获取'''

    pi = math.pi

    if not label_jsons or len(label_jsons) <= 1 or not perce_jsons[0].endswith('.json'):
        print('无3d检测标注数据')
        return

    configs = Config.replay_configs()
    enum_obstacle_type, analyze_obstacle_type = configs["enum_obstacle"], configs["analyze_obstacle"]
    columns = ['obstacle', 'yaw', 'Count']
    index = [x for x in analyze_obstacle_type]

    df = pd.DataFrame(columns=columns, index=index)
    df['obstacle'] = [x for x in index]
    df.fillna(0, inplace=True)

    for label_result, perce_result, fusion_result in utils.get_match_img_more_json(label_jsons, perce_jsons):
        if not label_result or not perce_result:
            continue
        for label_data, perce_data in utils.get_match_obstacle_3d(label_result, perce_result, fusion_result):
            if not perce_data or perce_data['obstacle_valid'] == 0:
                continue
            label_type = enum_obstacle_type[label_data['type']]

            label_yaw = label_data['rotation']['z']

            perce_yaw = perce_data["bbox3d"]['obstacle_heading_yaw']

            yaw_difference = abs(perce_yaw - label_yaw)

            degree_difference = ((yaw_difference) / pi) * 180

            if degree_difference > 180:
                degree_difference = 360 - degree_difference

            if degree_difference > 10:
                print("label_yaw is {}".format(label_yaw))
                print("perce_yaw is {}".format(perce_yaw))
                print("degree_difference is {}".format(degree_difference))

            result_type = label_type if label_type in analyze_obstacle_type else 'other'

            # if result_type != 'other':
            index_name = result_type
            df.loc[index_name, 'yaw'] += degree_difference
            df.loc[index_name, 'Count'] += 1

    df['yaw'] = df['yaw'] / df['Count']
    df['yaw'] = pd.to_numeric(df['yaw'].apply(lambda x: '%.4f' % x), errors='coerce')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df.fillna(0, inplace=True)
    utils.write_to_excel(df=df, file_name=file_name, sheet_name='yaw')


if __name__ == '__main__':
    lable_path = '/media/songbing/a47bfe5a-72ac-4ed4-9481-09bc5e37773a/caixin/version_test/4.1a/label/case2'
    perce_path = '/media/songbing/a47bfe5a-72ac-4ed4-9481-09bc5e37773a/SAIC_TDA4_playback/0720_4.2_new/img_record/image_record_3dcase2/image_record_json'
    lable_json_files = utils.get_all_files(lable_path, '.json')
    perce_json_files = utils.get_all_files(perce_path, '.json')

    str_time = (datetime.datetime.now()).strftime("%Y-%m-%d-%H-%M-%S")
    current_path = os.getcwd()
    range_filename = os.path.join(current_path,('range_' + str_time + '.xlsx'))

    #get_ranging_side(lable_json_files,perce_json_files,range_filename)
    #get_velocity_side(lable_json_files,perce_json_files,range_filename)
    #get_accel_side(lable_json_files,perce_json_files,range_filename)
    #get_dimension_side(lable_json_files,perce_json_files,range_filename)
    get_yaw_side(lable_json_files,perce_json_files,range_filename)
