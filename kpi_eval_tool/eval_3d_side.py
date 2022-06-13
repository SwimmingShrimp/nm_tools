import utils
import config
import pandas as pd
from datetime import datetime
import os
import json

class Eval3DSide:
    def __init__(self, lable_path, perce_path):
        self.lable_path = lable_path
        self.perce_path = perce_path
        self.current_path = os.getcwd()
    
    def add_track_id(file_path, save_file_path):
        lable_json_files = os.listdir(file_path)
        lable_json_files.sort(key=lambda x: x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6))

        idx = 0
        last_json_data = None

        for lable_json_file in lable_json_files:
            json_data = utils.get_json_data(lable_json_file)
            if idx >= 980:
                idx = 0
            if not last_json_data:
                for temp in json_data:
                    temp['id'] = idx
                    idx += 1
            else:
                json_data, idx = utils.add_track_id_helper(last_json_data, json_data, idx)

            last_json_data = json_data
            save_path = lable_json_file.replace(file_path, save_file_path)
            if not os.path.exists(os.path.dirname(save_path)):
                os.makedirs(os.path.dirname(save_path))
            with open(save_path, 'w') as f:
                json.dump(json_data, f, indent=4)
        return save_file_path

    def add_velocity(track_file_path):
        label_json_files = utils.get_json_list(track_file_path, '.json')
        label_json_files.sort(key=lambda x: x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6))

        queue = []
        for label_json_file in label_json_files:
            json_data = utils.get_json_data(label_json_file)
            queue.insert(0, json_data)
            if len(queue) <= 3:
                for temp in json_data:
                    temp["box_3d"]["velocity"] = {"x": -1000, "Y": -1000, "z": -1000}
            else:
                last_data = queue.pop()
                last_data_id = [x["id"] for x in last_data]
                for temp in json_data:
                    if temp["id"] in last_data_id:
                        last_temp = [x for x in last_data if x["id"] == temp["id"]][0]
                        temp["box_3d"]["velocity"] = {
                            "x": round((temp["box_3d"]["dists"]['x'] - last_temp["box_3d"]["dists"]["x"]) / 0.3, 3),
                            "y": round((temp["box_3d"]["dists"]['y'] - last_temp["box_3d"]["dists"]["y"]) / 0.3, 3),
                            "z": round((temp["box_3d"]["dists"]['z'] - last_temp["box_3d"]["dists"]["z"]) / 0.3, 3)
                        }
                    else:
                        temp["box_3d"]["velocity"] = {"x": -1000, "Y": -1000, "z": -1000}
            with open(label_json_file, 'w') as f:
                json.dump(json_data, f, indent=4)

    def add_accel(track_file_path):
        label_json_files = utils.get_json_list(track_file_path, '.json')
        label_json_files.sort(key=lambda x: x.rsplit('/', 1)[-1].rsplit('.')[0].rsplit('_')[-1].zfill(6))
        queue = []
        for label_json_file in label_json_files:
            json_data = utils.get_json_data(label_json_file)
            queue.insert(0, json_data)
            if len(queue) <= 3:
                for temp in json_data:
                    temp["box_3d"]["accel"] = {"x": -1000, "Y": -1000, "z": -1000}
            else:
                last_data = queue.pop()
                last_data_id = [x["id"] for x in last_data]
                for temp in json_data:
                    if temp["id"] in last_data_id and temp["box_3d"]["velocity"]["z"] != -1000:
                        last_temp = [x for x in last_data if x["id"] == temp["id"]][0]
                        if last_temp["box_3d"]["velocity"]["z"] == -1000:
                            temp["box_3d"]["accel"] = {"x": -1000, "Y": -1000, "z": -1000}
                            continue
                        temp["box_3d"]["accel"] = {
                            "x": round((temp["box_3d"]["velocity"]['x'] - last_temp["box_3d"]["velocity"]["x"]) / 0.3, 3),
                            "y": round((temp["box_3d"]["velocity"]['y'] - last_temp["box_3d"]["velocity"]["y"]) / 0.3, 3),
                            "z": round((temp["box_3d"]["velocity"]['z'] - last_temp["box_3d"]["velocity"]["z"]) / 0.3, 3)
                        }
                    else:
                        temp["box_3d"]["accel"] = {"x": -1000, "Y": -1000, "z": -1000}
            with open(label_json_file, 'w') as f:
                json.dump(json_data, f, indent=4)
    
    def proc_json_data(self):
        self.lable_path_3d = self.lable_path + '_3d'
        #获取所有的case目录
        self.case_path_list = []
        for root, _, _ in os.walk(self.lable_path):
            path_basename = os.path.basename(root)
            if 'case' in path_basename:
                self.case_path_list.append(root)
        for casename in self.case_path_list:
            lable_path_3d = self.lable_path + '_3d'
            save_file_path = os.path.join(lable_path_3d,os.path.basename(casename))
            track_file_path = Eval3DSide.add_track_id(casename, save_file_path)
            Eval3DSide.add_velocity(track_file_path)
            Eval3DSide.add_accel(track_file_path)


                

        