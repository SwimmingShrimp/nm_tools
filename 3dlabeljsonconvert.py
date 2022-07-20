#coding = utf-8
import json
import os
import argparse


def read_json_file(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
    return data


def check_path(file_path):
    folder = file_path[:file_path.rfind('/')]
    if not os.path.exists(folder):
        os.makedirs(folder)


def change_direction_name(direction_old, image_key_old):
    if 'rearleft' in direction_old:
        direction = 'side_left_rear'
        image_key = ('_').join(['frame', "vc5", str(int(image_key_old))])
    if 'frontleft' in direction_old:
        direction = 'side_left_front'
        image_key = ('_').join(['frame', "vc6", str(int(image_key_old))])
    if 'frontright' in direction_old:
        direction = 'side_right_front'
        image_key = ('_').join(['frame', "vc7", str(int(image_key_old))])
    if 'rearright' in direction_old:
        direction = 'side_right_rear'
        image_key = ('_').join(['frame', "vc8", str(int(image_key_old))])
    return direction, image_key


def get_lidar_data(frame_data):
    items_lidar = frame_data["items"]
    lidar_data = {}
    for item in items_lidar:
        i_data = {}
        xyz_veh = [item["position"]["x"], item["position"]["y"], item["position"]['z']]
        veh_type = item["category"]
        veh_dimension = item["dimension"]
        veh_rotation = item["rotation"]
        id = item['id']
        i_data['xyz_veh'] = xyz_veh
        i_data['type'] = veh_type
        i_data['dimension'] = veh_dimension
        i_data['rotation'] = veh_rotation
        i_data['label_id'] = id
        lidar_data[id] = i_data
    # print(lidar_data)
    #{'424c6c80-c284-43fb-a7e7-119aa9bd0a8a': 
    # {'dimension': {'y': 3.00274522236539, 'x': 15.058262380776918, 'z': 3.973050003356106}, 
    # 'xyz_veh': [49.44529976001691, -5.5178378019250856, 2.084936396609992], 
    # 'type': 'truck', 
    # 'rotation': {'y': 0, 'x': 0, 'z': -0.033149508742349044}
    # }
    return(lidar_data)


def get_image_data(frame_data,lidar_data):
    images_data = frame_data['images']
    res_images_data = []
    for image_data in images_data:
        res_data = {}
        image_path = image_data['image']
        image_side = image_path.split('/')[-2]
        image_name = image_path.split('/')[-1]
        image_boxs = []
        for item in image_data["items"]:
            i_box = {}
            id = item['id']
            category = item['category'].lower()
            box_2d = {}
            box_2d["x"] = item["position"]["x"]
            box_2d["y"] = item["position"]["y"]
            box_2d["w"] = item["dimension"]["x"]
            box_2d["h"] = item["dimension"]["y"]

            obstacle_type = {'undefined': 0, 'car': 1, 'truck': 2,'bus': 3,'pedestrian': 4,'bicycle': 5,'motorcycle': 6,'tricycle': 7,'barrier': 8,'cone': 9}
            type_value = obstacle_type[category]

            # bbox_xywh = [item["position"]["x"], item["position"]["y"],
            #             item["dimension"]["x"], item["dimension"]["y"]]
            if id not in lidar_data:
                print("Error:", id)
                continue
            lidar_box = lidar_data[id]
            xyz_veh = lidar_box['xyz_veh']
            global_dists = {}
            global_dists["x"] = xyz_veh[0]
            global_dists["y"] = xyz_veh[1]
            global_dists["z"] = xyz_veh[2]


            i_box['box_2d'] = box_2d
            i_box['type'] = type_value
            # i_box['label_id'] = id
            i_box['dimension'] = lidar_box['dimension']
            i_box['rotation'] = lidar_box['rotation']
            i_box['box_3d'] = {"global_dists": None}
            i_box['box_3d']["global_dists"] = global_dists


            image_boxs.append(i_box)
        res_data['image_side'] = image_side
        res_data['image_name'] = image_name
        res_data['image_boxs'] = image_boxs
        res_images_data.append(res_data)
    # print(res_images_data)
    return res_images_data


def process_single_json(frame_data,json_dir):
    lidar_data = get_lidar_data(frame_data)
    res_images_data = get_image_data(frame_data,lidar_data)
    casename = frame_data['frameUrl'].split('/')[5]
    for res_data in res_images_data:
        image_name = res_data['image_name']
        image_key_old = image_name.split('.')[0]
        new_json_dir = json_dir + "_new"
        direction_old = res_data["image_side"].lower()
        direction, image_key = change_direction_name(direction_old, image_key_old)
        new_side_dir = os.path.join(new_json_dir,casename, direction)
        new_json_file = os.path.join(new_side_dir, image_key + ".json")
        check_path(new_json_file)
        new_json_content = res_data["image_boxs"]
        # print(new_json_file)
        with open(new_json_file,'w') as f:
            json.dump(new_json_content,f,indent=4)
        

def process_json_list(json_list,json_dir):
    for file in json_list:
        data = read_json_file(file)
        frame_data =data['frames'][0]
        # print(frame_data)
        process_single_json(frame_data,json_dir)


def process(json_dir):
    all_json_files = []
    for roots, dirs, files in os.walk(json_dir):
        for file in files:
            file_path = os.path.join(roots,file)
            all_json_files.append(file_path)
    sorted(all_json_files)
    process_json_list(all_json_files,json_dir)


 
parser = argparse.ArgumentParser()
parser.add_argument('--json_dir', required=True, help = 'dir of json files')
args = parser.parse_args()


def main():
    json_dir = args.json_dir
    process(json_dir)


if __name__ == '__main__':
    main()
