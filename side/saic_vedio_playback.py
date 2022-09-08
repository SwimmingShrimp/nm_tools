import os
import cv2
import json
from argparse import ArgumentParser


def get_id(x):
    x = x.split('.')[0].split('_')
    if len(x) == 1:
        return int(x[0])
    elif len(x) > 1:
        return int(x[-1])


def main():
    parser = ArgumentParser()
    parser.add_argument('img_root_file', help='txt')
    parser.add_argument('config_file', help='absolut path for config')
    parser.add_argument('default_path', help='You know what is this')
    parser.add_argument('save_root', help='path to save videos and images')
    parser.add_argument('--fps', default=10, type=int)
    args = parser.parse_args()

    with open(args.img_root_file, 'r') as f:
        lines = f.readlines()
    
    if os.path.exists(args.save_root == False) and os.path.exists(args.save_root)==False:
        os.makedirs(args.save_root)
    video_root = os.path.join(args.save_root, 'video')
    image_root = os.path.join(args.save_root, 'images')
    if os.path.exists(video_root) == False:
        os.makedirs(video_root)
    if os.path.exists(image_root) == False:
        os.makedirs(image_root)
    
    ori = ['SideFrontLeft', 'SideFrontRight', 'SideRearLeft', 'SideRearRight']
    fourc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    for line in lines:
        line = line.strip()
        day = os.path.basename(line)
        for hour in os.listdir(line):
            img_hour_rt = os.path.join(line, hour)
            cars = os.listdir(img_hour_rt)
            car_ids = []
            for item in cars:
                code = item.split('-')[0]
                if code not in car_ids:
                    car_ids.append(code)
            for idx in car_ids:
                SFL_root = os.path.join(img_hour_rt, idx+'-'+ori[0])
                SFR_root = os.path.join(img_hour_rt, idx+'-'+ori[1])
                SRL_root = os.path.join(img_hour_rt, idx+'-'+ori[2])
                SRR_root = os.path.join(img_hour_rt, idx+'-'+ori[3])
                with open(args.config_file, 'r') as f:
                    jsdicts = json.load(f)
                jsdicts['offline']['image_root'] = img_hour_rt

                if os.path.exists(SFL_root) and os.path.exists(SFR_root) and os.path.exists(SRL_root) and os.path.exists(SRR_root):
                    save_path = os.path.join(image_root, day, hour, idx)
                    if os.path.exists(save_path):
                        continue
                    else:
                        os.makedirs(save_path)
                    len_sfl = len(os.listdir(SFL_root))
                    len_sfr = len(os.listdir(SFR_root))
                    len_srl = len(os.listdir(SRL_root))
                    len_srr = len(os.listdir(SRR_root))
                    end_index = min(len_sfl, len_sfr, len_srl, len_srr)
                    jsdicts['offline']['finish_index'] = end_index
                    jsdicts['offline']['camera_name'] = [idx+'-'+ori[2], idx+'-'+ori[0], idx+'-'+ori[1], idx+'-'+ori[3]]
                    jsstr = json.dumps(jsdicts, indent=4)
                    with open(args.config_file, 'w') as f:
                        f.write(jsstr)
                    os.system('./obstacle_inference_main {}'.format(args.config_file))                    
                    os.system('mv {}/* {}'.format(args.default_path, save_path))
                    print('generating videos')
                    save_path2 = os.path.join(video_root, day, hour, idx)
                    if os.path.exists(save_path2) ==False:
                        os.makedirs(save_path2)
                    savename = []
                    for i in range(4):
                        img_for_camera = os.path.join(save_path, 'image_record_pic', idx+'-'+ori[i])
                        video_save_name = os.path.join(save_path2, '{}.avi'.format(ori[i]))
                        videoWriter = cv2.VideoWriter(video_save_name, fourc, args.fps, (640, 384))
                        imglist = os.listdir(img_for_camera)
                        imglist = sorted([fn for fn in imglist], key=get_id)
                        for item in imglist:
                            imgp = os.path.join(img_for_camera, item)
                            frame = cv2.imread(imgp)
                            videoWriter.write(frame)
                        videoWriter.release()
                else:
                    print('Path:{}\nCar_id"{}\nCamera is not enough for this car id')
                    continue
if __name__ == '__main__':
    main()
                



                


