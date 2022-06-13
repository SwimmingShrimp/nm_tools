side_2d_config = {
    'iou' : 0.5,
    'topcut': 200,
    'proportion':3.75,
    'obstacle_type' : ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle'],
    'enum_obstacle': {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',7: 'tricycle'},
    'subclass_type' : ['car', 'truck', 'bus'],
    'class_subclass_type' : ['car_sedan', 'car_hatchback', 'car_other', 'truck_big', 'truck_small', 'truck_other', 'bus_big', 'bus_small', 'bus_other'],
    'car' : {0: 'sedan', 1: 'hatchback', 2:'other'},
    'truck': {0: 'big', 1: 'small', 2:'other'},
    'bus': {0: 'big', 1: 'small', 2:'other'}
}

side_3d_config = {
    'iou' : 0.5,
    'topcut': 200,
    'proportion':3.75,
    'obstacle_type' : ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle'],
    'enum_obstacle': {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',7: 'tricycle'},
    'subclass_type' : ['car', 'truck', 'bus'],
    'class_subclass_type' : ['car_sedan', 'car_hatchback', 'car_other', 'truck_big', 'truck_small', 'truck_other', 'bus_big', 'bus_small', 'bus_other'],
    'car' : {0: 'sedan', 1: 'hatchback', 2:'other'},
    'truck': {0: 'big', 1: 'small', 2:'other'},
    'bus': {0: 'big', 1: 'small', 2:'other'}
}

front_2d_config = {
    'iou' : 0.5,
    'topcut': 0,
    'topadd': 72,
    'proportion':3,
    'obstacle_type' : ['car', 'truck', 'bus', 'pedestrian', 'bicycle', 'motorcycle', 'tricycle'],
    'enum_obstacle': {1: 'car', 2: 'truck', 3: 'bus', 4: 'pedestrian', 5: 'bicycle', 6: 'motorcycle',7: 'tricycle'}
}