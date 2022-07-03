import os
import json
import argparse
import cv2
import numpy as np
from pathlib import Path



def read_json_file(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
    return data


def main():
    json_dir = args.json_dir
    img_dir = args.img_dir
    print('json_dir is {}'.format(json_dir))
    print('img_dir is {}'.format(img_dir))

    json_path_lf = []
    json_path_rf = []
    json_path_lr = []
    json_path_rr = []
    json_path_fusion = []

    img_path_lf = []
    img_path_rf = []
    img_path_lr = []
    img_path_rr = []



    for roots, dirs, files in os.walk(json_dir):
        for file_ in files:
            json_path = os.path.join(roots,file_)
            if 'left_front' in json_path:
                json_path_lf.append(json_path)
            elif 'right_front' in json_path:
                json_path_rf.append(json_path)
            elif 'left_rear' in json_path:
                json_path_lr.append(json_path)
            elif 'right_rear' in json_path:
                json_path_rr.append(json_path)
            elif 'fusion' in json_path:
                json_path_fusion.append(json_path)


    for roots, dirs , files in os.walk(img_dir):
        for file_ in files:
            img_path = os.path.join(roots,file_)
            if 'left_front' in img_path:
                img_path_lf.append(img_path)
            elif 'right_front' in img_path:
                img_path_rf.append(img_path)
            elif 'left_rear' in img_path:
                img_path_lr.append(img_path)
            elif 'right_rear' in img_path:
                img_path_rr.append(img_path)

    json_path_lf.sort(key = lambda x: (x.rsplit('/', 1)[-1].split('.')[0]))
    json_path_rf.sort(key = lambda x: (x.rsplit('/', 1)[-1].split('.')[0]))
    json_path_lr.sort(key = lambda x: (x.rsplit('/', 1)[-1].split('.')[0]))
    json_path_rr.sort(key = lambda x: (x.rsplit('/', 1)[-1].split('.')[0]))
    json_path_fusion.sort(key = lambda x: (x.rsplit('/', 1)[-1].split('.')[0]))


    for i, json in enumerate(json_path_fusion):
        print (i)
        
        '''
        left_front
        '''
        json_num = int(os.path.basename(json).split('.')[0])

        for img_lf_ in img_path_lf:
            img_name = os.path.basename(img_lf_).split('.')[0]
            if 'left_front' in img_name:
                img_num = int(img_name.rsplit('_')[-1])
            else:
                pass

            if img_num == json_num:
                img_lf = cv2.imread(img_lf_)
                break
            else:
                img_lf = np.zeros((256,512,3), np.uint8)
                img_lf.fill(255)

        cv2.putText(img_lf, ('Left_Front  ' + str(i)),(5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))


        data_lf = read_json_file(json_path_lf[i])
        obstacles_lf = data_lf['tracks']
        if obstacles_lf is None:
            pass
        else:
            for obstacle in obstacles_lf:
                id = obstacle['obstacle_id']
                x = obstacle['uv_bbox2d']['obstacle_bbox.x']
                y = obstacle['uv_bbox2d']['obstacle_bbox.y']
                w = obstacle['uv_bbox2d']['obstacle_bbox.width']
                h = obstacle['uv_bbox2d']['obstacle_bbox.height']
                obstacle_type = obstacle['obstacle_type']
                cv2.rectangle(img_lf, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 1)
                

                if (y) > 10:
                    cv2.putText(img_lf, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) - 6), cv2.FONT_HERSHEY_PLAIN, 
                                0.8, (0, 255, 0))
                else:
                    cv2.putText(img_lf, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) + 15), cv2.FONT_HERSHEY_PLAIN,
                                0.8, (0, 255, 0))


        '''
        right_front
        '''


        for img_rf_ in img_path_rf:
            img_name = os.path.basename(img_rf_).split('.')[0]
            
            if 'right_front' in img_name:
                img_num = int(img_name.rsplit('_')[-1])
            else:
                pass

            if img_num == json_num:
                img_rf = cv2.imread(img_rf_)
                break
            else:
                img_rf = np.zeros((256,512,3), np.uint8)
                img_rf.fill(255)


        cv2.putText(img_rf, ('Right_Front  ' + str(i)),(5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))

        data_rf = read_json_file(json_path_rf[i])
        obstacles_rf = data_rf['tracks']
        if obstacles_rf is None:
            pass
        else:
            for obstacle in obstacles_rf:
                id = obstacle['obstacle_id']
                x = obstacle['uv_bbox2d']['obstacle_bbox.x']
                y = obstacle['uv_bbox2d']['obstacle_bbox.y']
                w = obstacle['uv_bbox2d']['obstacle_bbox.width']
                h = obstacle['uv_bbox2d']['obstacle_bbox.height']
                obstacle_type = obstacle['obstacle_type']
                cv2.rectangle(img_rf, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 1)
                

                if (y) > 10:
                    cv2.putText(img_rf, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) - 6), cv2.FONT_HERSHEY_PLAIN, 
                                0.8, (0, 255, 0))
                else:
                    cv2.putText(img_rf, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) + 15), cv2.FONT_HERSHEY_PLAIN,
                                0.8, (0, 255, 0))
        

        '''
        left_rear
        '''



        for img_lr_ in img_path_lr:
            img_name = os.path.basename(img_lr_).split('.')[0]


            if 'left_rear' in img_name:
                img_num = int(img_name.rsplit('_')[-1])
            else:
                pass




            if img_num == json_num:
                img_lr = cv2.imread(img_lr_)
                break
            else:
                img_lr = np.zeros((256,512,3), np.uint8)
                img_lr.fill(255)


        cv2.putText(img_lr, ('Left_Rear  ' + str(i)),(5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))

        data_lr = read_json_file(json_path_lr[i])
        obstacles_lr = data_lr['tracks']
        if obstacles_lr is None:
            pass
        else:
            for obstacle in obstacles_lr:
                id = obstacle['obstacle_id']
                x = obstacle['uv_bbox2d']['obstacle_bbox.x']
                y = obstacle['uv_bbox2d']['obstacle_bbox.y']
                w = obstacle['uv_bbox2d']['obstacle_bbox.width']
                h = obstacle['uv_bbox2d']['obstacle_bbox.height']
                obstacle_type = obstacle['obstacle_type']
                cv2.rectangle(img_lr, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 1)
                

                if (y) > 10:
                    cv2.putText(img_lr, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) - 6), cv2.FONT_HERSHEY_PLAIN, 
                                0.8, (0, 255, 0))
                else:
                    cv2.putText(img_lr, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) + 15), cv2.FONT_HERSHEY_PLAIN,
                                0.8, (0, 255, 0))

        '''
        right_rear
        '''



        for img_rr_ in img_path_rr:
            img_name = os.path.basename(img_rr_).split('.')[0]
            
            if 'right_rear' in img_name:
                img_num = int(img_name.rsplit('_')[-1])
            else:
                pass


            if img_num == json_num:
                img_rr = cv2.imread(img_rr_)
                break
            else:
                img_rr = np.zeros((256,512,3), np.uint8)
                img_rr.fill(255)

        cv2.putText(img_rr, ('Right_Rear  ' + str(i)),(5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))

        data_rr = read_json_file(json_path_rr[i])
        obstacles_rr = data_rr['tracks']
        if obstacles_rr is None:
            pass
        else:
            for obstacle in obstacles_rr:
                id = obstacle['obstacle_id']
                x = obstacle['uv_bbox2d']['obstacle_bbox.x']
                y = obstacle['uv_bbox2d']['obstacle_bbox.y']
                w = obstacle['uv_bbox2d']['obstacle_bbox.width']
                h = obstacle['uv_bbox2d']['obstacle_bbox.height']
                obstacle_type = obstacle['obstacle_type']
                cv2.rectangle(img_rr, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 1)
                

                if (y) > 10:
                    cv2.putText(img_rr, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) - 6), cv2.FONT_HERSHEY_PLAIN, 
                                0.8, (0, 255, 0))
                else:
                    cv2.putText(img_rr, (str(id) + " type:" + str(obstacle_type)), (int(x), int(y) + 15), cv2.FONT_HERSHEY_PLAIN,
                                0.8, (0, 255, 0))

        '''
        BEV
        '''
        img_bev = np.zeros((512,300,3), np.uint8)
        img_bev.fill(200)
        cv2.putText(img_bev, ('BEV  ' + str(i)),(5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
        data_bev = read_json_file(json_path_fusion[i])
        obstacles_bev = data_bev['tracks']

        me_x = 150
        me_y = 244

        cv2.rectangle(img_bev, (145, 244), (155, 269), (255, 255, 0), -1)

        if obstacles_bev is None:
            pass
        else:
            for obstacle in obstacles_bev:
                id = obstacle['obstacle_id']
                obstacle_x = obstacle["position"]["obstacle_pos_y_filter"]
                obstacle_y = obstacle["position"]["obstacle_pos_x_filter"]
                w = obstacle["obstacle_width"]
                h = obstacle["obstacle_length"]
                obstacle_type = obstacle['obstacle_type']

                if abs(obstacle_x) > 15 or abs(obstacle_y) > 60:
                    continue

                x = int(me_x - (obstacle_x * 5))
                y = int(me_y - (obstacle_y * 5))


                cv2.rectangle(img_bev, (int(x-w*2.5), int(y-h*2.5)), (int(x+w*2.5), int(y+ h*2.5)), (0, 255, 0), -1)
                cv2.putText(img_bev, str(id), (int(x-w*2.5), int(y+ h*2.5) + 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 255, 0))
                

        img = np.vstack([np.hstack([img_lf, img_rf]), np.hstack([img_lr, img_rr])])
        img = np.vstack([np.hstack([img,img_bev])])

        save_path = os.path.join(str(img_dir) + '_new')
        img_path = os.path.join(str(save_path),str(os.path.basename(json).split('.')[0])+'.png')
        cv2.line(img,(0,256),(1024,256),color = (0,0,0),thickness = 1)
        cv2.line(img,(512,0),(512,512),color = (0,0,0),thickness = 1)
        cv2.line(img,(1024,0),(1024,512),color = (0,0,0),thickness = 1)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        cv2.imwrite(img_path, img)
        # cv2.imshow('image', img)
        # cv2.waitKey(1000)
        



parser = argparse.ArgumentParser(description = 'real car json path and img path')
parser.add_argument('--json_dir', required=True, help = 'path of json files')
parser.add_argument('--img_dir', required=True, help = 'path of img files')
args = parser.parse_args()


if __name__ == '__main__':
    main()
