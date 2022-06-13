# coding='utf-8'
import os
import utils
import json

image_root = '/home/NULLMAX/lixialin/文档/tools/images_root.txt'
data_json = '/home/NULLMAX/lixialin/文档/project/preception_side/obstacle_perception/data/obstacle_perception_1.json'
dst_data_json = '/home/NULLMAX/lixialin/文档/project/preception_side/obstacle_perception/data/obstacle_perception_2.json'
dst_dir = '/home/NULLMAX/lixialin/文档/project/preception_side/obstacle_perception/build_infer/x86_linux'
with open(data_json, 'r',encoding='utf-8') as f1:
    json_data = json.load(f1)
with open(image_root,'r') as f:
    lines =f.readlines()
    for line in lines:
        print(line)
        json_data["offline"]["image_root"]=line
        with open(dst_data_json,'w') as f2:
            json.dump(json_data,f2,indent=4)
        dirname_prec = os.path.dirname(line)
        command = './obstacle_inference_main {}'.format(data_json)
        os.chdir(dst_dir)
        os.system(command)
        prec_json = dirname_prec + '/prec_json'
        if not prec_json:
            os.mkdirs(prec_json)
        command1 = ('mv {}/image_record/image_record_json {}'.format(dst_dir,prec_json))
        print(command1)
        os.system(command1)
