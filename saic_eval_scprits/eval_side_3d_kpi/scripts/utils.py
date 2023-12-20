# -*- coding: utf-8 -*-
import copy
import logging
import os
import json

from datetime import datetime
import cv2
import pandas as pd

from config.cfg import Config

FUNCTION_SET = {}
BASIC_NAME = os.path.dirname(os.path.dirname(__file__)) + '/data/' + datetime.now().strftime("%Y_%m_%d_")


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    log_filename = os.path.dirname(os.path.dirname(__file__)) + "/log/" + datetime.now().strftime(
        "%Y_%m_%d_%H_%M_%S") + ".log"
    fh = logging.FileHandler(log_filename, mode='w')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(stream_handler)
    return logger


def write_to_excel(df, file_name, sheet_name):
    print('-·-' * 30)
    print(df)
    writer = pd.ExcelWriter(file_name)
    if os.path.exists(file_name):
        raw_df = pd.read_excel(file_name, sheet_name=None)
        for sheet, data in raw_df.items():
            if sheet == sheet_name:
                df = pd.concat([data, df], sort=False)
            else:
                data.to_excel(excel_writer=writer, sheet_name=sheet, index=False, engine='openpyxl')
    df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False, engine='openpyxl')
    writer.save()


def get_all_files(path, file_extension):
    files = []
    list_dir = os.listdir(path)
    for each in list_dir:
        each_path = os.path.join(path, each)
        if os.path.isdir(each_path):
            files.extend(get_all_files(each_path, file_extension))
        if os.path.isfile(each_path) and each_path.endswith(file_extension):
            files.append(each_path)
    return files


def get_bag_msg(file_path, topic_list):
    bags = get_all_files(file_path, '.bag')
    bags.sort(reverse=False)
    bag_count = 0
    for bag_path in bags:
        logger.info('开始处理：{}'.format(os.path.basename(bag_path)))
        try:
            bag_data = rosbag.Bag(bag_path, skip_index=True)
            bag_count += 1
        except:
            continue
        for topic, msg, t in bag_data.read_messages(
                topics=topic_list):
            yield topic, msg, t, bag_path, bag_count
        bag_data.close()


def register(problem_type, mod):
    def add(fn):
        FUNCTION_SET[problem_type] = [fn.__name__, mod]

        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return add


def is_in_poly(p, poly):
    px, py = p
    poly = list(poly)
    is_in = False
    for i, corner in enumerate(poly):
        next_i = i + 1 if i + 1 < len(poly) else 0
        x1, y1 = corner
        x2, y2 = poly[next_i]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):
            is_in = True
            break
        if min(y1, y2) < py <= max(y1, y2):
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:
                is_in = True
                break
            elif x > px:
                is_in = not is_in
    return is_in


def dump_problem_data(file_name, label_data, raw_perce_result, mod):
    file_path = os.path.join(os.path.dirname(BASIC_NAME), mod, 'json-' + datetime.now().strftime("%d-%H%M"))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path, file_name).rsplit('.', 1)[0] + '.json'
    if os.path.exists(file_path):
        problems_json_data = get_json_data(file_path)
    else:
        problems_json_data = {"task_vehicle": [], "tracks": {}}
    problems_json_data["tracks"].update(raw_perce_result)
    problems_json_data['filename'] = file_name
    problems_json_data["task_vehicle"].append(label_data)
    with open(file_path, 'w') as f:
        json.dump(problems_json_data, f, indent=4)


def bb_intersection_over_union(boxA, boxB):
    A11 = boxA["obstacle_bbox.x"]
    A12 = boxA["obstacle_bbox.x"] + boxA["obstacle_bbox.width"]
    A21 = boxA["obstacle_bbox.y"]
    A22 = boxA["obstacle_bbox.y"] + boxA["obstacle_bbox.height"]

    B11 = boxB["obstacle_bbox.x"]
    B12 = boxB["obstacle_bbox.x"] + boxB["obstacle_bbox.width"]
    B21 = boxB["obstacle_bbox.y"]
    B22 = boxB["obstacle_bbox.y"] + boxB["obstacle_bbox.height"]

    areaA = boxA["obstacle_bbox.height"] * boxA["obstacle_bbox.width"]
    areaB = boxB["obstacle_bbox.height"] * boxB["obstacle_bbox.width"]

    interW = max(0, min(A12, B12) - max(A11, B11))
    interH = max(0, min(A22, B22) - max(A21, B21))

    interArea = interH * interW
    iou = interArea / (areaA + areaB - interArea)
    return iou


def get_json_data(json_file):
    with open(json_file) as f:
        try:
            json_data = json.load(f)
        except:
            logger.info('json文件加载失败：{}'.format(json_file))
            return None
        return json_data


def get_match_img_one_json(label_jsons, perce_jsons):
    label_data = get_json_data(label_jsons[0])
    label_jsons_name = [temp["filename"].rsplit('.')[0] for temp in label_data]
    perce_jsons = [file for file in perce_jsons if file.rsplit('/')[-1].split('.')[0] in label_jsons_name]
    perce_jsons.sort(key=lambda x: x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6))
    perce_jsons.sort(key=lambda x: x.rsplit('/', 1)[0])
    if not label_jsons or not perce_jsons:
        logger.info('无可匹配标注图片数据')
        yield None, None
        return

    for perce_json in perce_jsons:
        for label_result in label_data:
            if perce_json.split('/')[-1].split('.')[0] == label_result["filename"].split('.')[0]:
                perce_result = get_json_data(perce_json)
                yield label_result, perce_result
                break


def get_match_img_more_json(label_jsons, perce_jsons):
    label_jsons_name = [name.rsplit('/')[-1].split('.')[0] for name in label_jsons]
    # print("label_jsons_name is "+ str(label_jsons_name))
    #label_jsons_name = ['frame_vc7_3', 'frame_vc7_1', 'frame_vc7_2', 'frame_vc7_0'...]

    fusion_jsons = [file for file in perce_jsons if 'camera_fusion' in file]
    fusion_path = fusion_jsons[0].rsplit('/', 1)[0]
    perce_jsons = [file for file in perce_jsons if file.split('/')[-1].split('.')[0] in label_jsons_name]
    # print("perce_jsons is "+ str(perce_jsons))
    # ['/home/NULLMAX/caixin/temp/3dfusiontest/result/side_right_front/frame_vc7_3.json', ...




    perce_jsons.sort(key=lambda x: (x.rsplit('/', 1)[-1].split('_')[1][2],
                                    x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6)))
    label_jsons.sort(key=lambda x: (x.rsplit('/', 1)[-1].split('_')[1][2],
                                    x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6)))

    # print('perce_jsons are ' + str(perce_jsons))
    # print('label_jsons are ' + str(label_jsons))



    if not label_jsons or not label_jsons:
        logger.info('无可匹配标注图片数据')
        yield None, None
        return

    for perce_json in perce_jsons:
        for label_json in label_jsons:
            if  perce_json.split('/')[-1] == label_json.split('/')[-1]:
                print("label_json is {}".format(label_json))
                fusion_id = perce_json.rsplit('_')[-1]
                fusion_json = os.path.join(fusion_path, fusion_id)

                label_result = get_json_data(label_json)
                perce_result = get_json_data(perce_json)
                fusion_result = get_json_data(fusion_json)
                # print(fusion_result)
                yield label_result, perce_result, fusion_result
                break


def get_match_obstacle_recall_side(label_result, perce_result):
    raw_perce_result = copy.deepcopy(perce_result)
    perce_result = perce_result["tracks"]
    configs = Config.replay_configs()
    line_compensation = configs["using_cfg"]["line_compensation"]
    proportion = configs["using_cfg"]["proportion"]
    iou_benchmark = configs['iou']
    for label_data in label_result["task_vehicle"]:
        boxA = {}
        boxA["obstacle_bbox.height"] = label_data['tags']['height'] / proportion
        boxA["obstacle_bbox.width"] = label_data['tags']['width'] / proportion
        boxA["obstacle_bbox.x"] = label_data['tags']['x'] / proportion
        boxA["obstacle_bbox.y"] = (label_data['tags']['y'] + line_compensation) / proportion

        is_in = False
        px = boxA["obstacle_bbox.x"] * proportion + boxA["obstacle_bbox.width"] * proportion / 2
        py = boxA["obstacle_bbox.y"] * proportion - line_compensation + boxA["obstacle_bbox.height"] * proportion / 2
        point = [px, py]  

        occluded = label_data['tags']['occluded']
        attention_areas = label_result["task_attention_area"]
        if int(occluded) != 0:
            continue
        for attention_area in attention_areas:
            xn = [float(x) for x in attention_area["tags"]["xn"].replace('"', '').split(';')]
            yn = [float(y) for y in attention_area["tags"]["yn"].replace('"', '').split(';')]
            polygon = zip(xn, yn)
            if is_in_poly(point, polygon):
                is_in = True
                break
        if not is_in:
            continue
        if not perce_result:
            yield label_data, None
            continue

        iou_result = {}
        for i in range(len(perce_result)):
            boxB = perce_result[i]["uv_bbox2d"]
            iou = bb_intersection_over_union(boxA, boxB)
            iou_result[i] = iou
        iou_max_item = max(iou_result.items(), key=lambda x: x[1])
        iou_max_value = iou_max_item[1]
        iou_max_id = iou_max_item[0]
        if iou_max_value >= iou_benchmark:
            yield label_data, perce_result[iou_max_id]
            del perce_result[iou_max_id]
        else:
            if label_data['tags']["class"] != 'wheel' and label_data['tags']["class"] != 'cone' \
                    and label_data['tags']["class"] != 'safety-crash-barrels':
                label_data['tags']["problem"] = 'FN'
                dump_problem_data(label_result['filename'], label_data, raw_perce_result["tracks"][0], 'recall')
            yield label_data, None


def get_match_obstacle_precision_side(label_result, perce_result):
    perce_result = perce_result["tracks"]
    attention_areas = label_result["task_attention_area"]
    configs = Config.replay_configs()
    line_compensation = configs["using_cfg"]["line_compensation"]
    proportion = configs["using_cfg"]["proportion"]
    iou_benchmark = configs['iou']
    for label_data in label_result["task_vehicle"]:
        boxA = {}
        boxA["obstacle_bbox.height"] = label_data['tags']['height'] / proportion
        boxA["obstacle_bbox.width"] = label_data['tags']['width'] / proportion
        boxA["obstacle_bbox.x"] = label_data['tags']['x'] / proportion
        boxA["obstacle_bbox.y"] = (label_data['tags']['y'] + line_compensation) / proportion

        is_in = False
        px = boxA["obstacle_bbox.x"] * proportion + boxA["obstacle_bbox.width"] * proportion / 2
        py = boxA["obstacle_bbox.y"] * proportion - line_compensation + boxA["obstacle_bbox.height"] * proportion / 2
        point = [px, py]
        occluded = label_data['tags']['occluded']
        for attention_area in attention_areas:
            xn = [float(x) for x in attention_area["tags"]["xn"].replace('"', '').split(';')]
            yn = [float(y) for y in attention_area["tags"]["yn"].replace('"', '').split(';')]
            polygon = zip(xn, yn)
            if is_in_poly(point, polygon):
                is_in = True
                break
        if not perce_result:
            yield None, None
            return
        iou_result = {}
        for i in range(len(perce_result)):
            boxB = perce_result[i]["uv_bbox2d"]
            iou = bb_intersection_over_union(boxA, boxB)
            iou_result[i] = iou
        iou_max_item = max(iou_result.items(), key=lambda x: x[1])
        iou_max_value = iou_max_item[1]
        iou_max_id = iou_max_item[0]
        if iou_max_value >= iou_benchmark:
            if int(occluded) == 0 and is_in:
                yield label_data, perce_result[iou_max_id]
            del perce_result[iou_max_id]
            continue

    if perce_result:
        for i in range(len(perce_result)):
            perce_data = perce_result[i]
            if abs(perce_data["bbox3d"]["obstacle_pos_x"]) > 60 or abs(perce_data["bbox3d"]["obstacle_pos_y"]) >15 :
                continue
            px = perce_data["uv_bbox2d"]["obstacle_bbox.x"] * proportion + perce_data["uv_bbox2d"][
                "obstacle_bbox.width"] * proportion / 2
            py = perce_data["uv_bbox2d"]["obstacle_bbox.y"] * proportion - line_compensation + perce_data["uv_bbox2d"][
                "obstacle_bbox.height"] * proportion / 2
            pointcenter = [px, py]
            for attention_area in attention_areas:
                xn = [float(x) for x in attention_area["tags"]["xn"].replace('"', '').split(';')]
                yn = [float(y) for y in attention_area["tags"]["yn"].replace('"', '').split(';')]
                polygon = zip(xn, yn)
                if is_in_poly(pointcenter, polygon) == True:
                    for label_data in label_result["task_vehicle"]:
                        perce_data['problem'] = 'FP'
                        if int(label_data['tags']['occluded']) != 0 \
                                and label_data['tags']['type'] != 'wheel' \
                                and label_data['tags']['type'] != 'cone' \
                                and label_data['tags']["class"] != 'safety-crash-barrels':
                            dump_problem_data(label_result['filename'], label_data, perce_data, 'precision')
                    yield None, perce_data


def get_match_obstacle_3d(label_result, perce_result, fusion_result):
    perce_result = perce_result["tracks"]
    fusion_result = fusion_result["tracks"]
    configs = Config.replay_configs()
    line_compensation = configs["using_cfg"]["line_compensation"]
    proportion = configs["using_cfg"]["proportion"]
    iou_benchmark = configs['iou']
    for label_data in label_result:
        if not perce_result:
            continue
        boxA = {}
        boxA["obstacle_bbox.height"] = label_data["box_2d"]['h'] / proportion
        boxA["obstacle_bbox.width"] = label_data["box_2d"]['w'] / proportion
        boxA["obstacle_bbox.x"] = label_data["box_2d"]['x'] / proportion
        boxA["obstacle_bbox.y"] = (label_data["box_2d"]['y'] + line_compensation) / proportion
        iou_result = {}
        for i in range(len(perce_result)):
            perce_data = perce_result[i]
            # boxB1 = perce_data["uv_bbox2d"]
            boxB = perce_data["uv_bbox2d"]
            # h = boxB1["obstacle_bbox.height"]
            # w = boxB1["obstacle_bbox.width"]
            # x = boxB1["obstacle_bbox.x"]
            # y = boxB1["obstacle_bbox.y"]
            # boxB["obstacle_bbox.x"]= x -w/2
            # boxB["obstacle_bbox.y"]= y -h/2

            iou = bb_intersection_over_union(boxA, boxB)
            iou_result[i] = iou
        iou_max_item = max(iou_result.items(), key=lambda x: x[1])
        # print("iou_max_item is " + str(iou_max_item))

        iou_max_value = iou_max_item[1]
        iou_max_id = iou_max_item[0]
        if iou_max_value >= iou_benchmark:

            ioumax_perceresult = perce_result[iou_max_id]
            one_side_id = ioumax_perceresult["obstacle_id"]

            if fusion_result is None:
                continue
            else:
                for obstacle in fusion_result:
                    fusion_side_id = obstacle["obstacle_id"]
                    if fusion_side_id == one_side_id:
                        # yield label_data, perce_result[iou_max_id]
                        # print(obstacle)
                        yield label_data, obstacle
                        del perce_result[iou_max_id]
                    else:
                        pass





def draw_plot(new_path, problem_json_data):
    configs = Config.replay_configs()
    line_compensation = configs["using_cfg"]["line_compensation"]
    proportion = configs["using_cfg"]["proportion"]
    img_data = cv2.imread(new_path)
    if problem_json_data.get("task_vehicle"):
        for temp in problem_json_data["task_vehicle"]:
            A11 = temp["tags"]["x"]
            A21 = temp["tags"]["y"]
            A12 = temp["tags"]["width"] + A11
            A22 = temp["tags"]["height"] + A21
            problem = temp["tags"].get("problem")
            if problem:
                labelSize = cv2.getTextSize(problem, cv2.FONT_HERSHEY_COMPLEX, 0.5, 1)
                x_text = int(A11) + labelSize[0][0]
                y_text = int(A21) - int(labelSize[0][1])
                cv2.rectangle(img_data, (int(A11), int(A21)), (x_text, y_text), (255, 0, 0), cv2.FILLED)
                cv2.putText(img_data, problem, (int(A11), int(A21)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)
            cv2.rectangle(img_data, (int(A11), int(A21)), (int(A12), int(A22)), (255, 0, 0), 2)
    if problem_json_data.get("tracks"):
        for key, perce in problem_json_data["tracks"].items():
            A11 = perce["uv_bbox2d"]["obstacle_bbox.x"] * proportion
            A21 = perce["uv_bbox2d"]["obstacle_bbox.y"] * proportion - line_compensation
            A12 = perce["uv_bbox2d"]["obstacle_bbox.width"] * proportion + A11
            A22 = perce["uv_bbox2d"]["obstacle_bbox.height"] * proportion + A21
            cv2.rectangle(img_data, (int(A11), int(A21)), (int(A12), int(A22)), (0, 255, 0), 2)
            problem = perce.get('problem')
            if problem:
                labelSize = cv2.getTextSize(problem, cv2.FONT_HERSHEY_COMPLEX, 0.5, 1)
                x_text = int(A11) + labelSize[0][0]
                y_text = int(A21) - int(labelSize[0][1])
                cv2.rectangle(img_data, (int(A11), int(A21)), (x_text, y_text), (0, 255, 0), cv2.FILLED)
                cv2.putText(img_data, str(key) + problem, (int(A11), int(A21)), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                            (0, 0, 0), 1)
    cv2.imwrite(new_path.replace('.yuv', '.png'), img_data)


logger = init_logger()
