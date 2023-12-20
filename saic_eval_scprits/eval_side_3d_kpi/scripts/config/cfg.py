import numpy as np
from pprint import pprint


class Config:
    def __init__(self):
        self.evalcfgs = {
            'conf_thre': 0.001,
            'iou_thres': np.linspace(0.5, 0.95, 10, endpoint=True),
            'recall_thres': np.linspace(.0, 1.00, 101, endpoint=True),
            'max_dets': [1, 10, 100],
            'fn_ios_thre': 0.2,
            'fp_ios_thre': 0.5,
            'ign_ios_thre': 0.5,
            'cate_miscls_iou_thre': 0.5,
            'area_types': ['all', 'small', 'medium', 'large'],
            'area_ranges': [(0 ** 2, 1e5 ** 2), (0 ** 2, 32 ** 2), (32 ** 2, 96 ** 2), (96 ** 2, 1e5 ** 2)],
            'catenms': ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle', 'barrier',
                        'cone', 'sign', 'lock', 'None']
        }
        # print('\n==> (cfg.py) default evalcfgs: ')
        # pprint(self.evalcfgs)

    @classmethod
    def replay_configs(cls):
        configs = {
            "using_cfg": {"line_compensation": -200, "proportion": 3.75},
            "iou": 0.5,
            "enum_obstacle": {0: 'undefined', 1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle',
                              6: 'motorcycle', 7: 'tricycle', 8: 'misc', 9: 'cone', 10: 'barrier', 11: 'barrel', 12: 'tripod'},
            # "analyze_obstacle": ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle', 'rider'],
            "analyze_obstacle": ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle'],
            "SML_obstacle_cfg": {'small': (0, 1024), 'middle': (1024, 9216), 'large': (9216, 200000)},
            "ranging_obstacle_x": {'0~20': (0, 20), '20~35': (20, 35), '35~60': (35, 60)},
            "ranging_obstacle_y": {'first': (1, 4.5), 'second': (3.5, 7), 'third': (6, 12.5), 'Xrange': (0, 12.5)},
        }
        return configs
