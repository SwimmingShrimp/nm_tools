import os
import cv2
import sys
sys.path.append('../..')
import utils
import numpy as np

pic = '/home/lixialin/Videos/0511_new/back_rp/pic_ori'
gt_json_path = '/home/lixialin/Videos/0511_new/back_rp/gt_json'
dst = '/home/lixialin/Videos/0511_new/back_rp/pic_gt'
os.makedirs(dst,exist_ok=True)

def draw_gt(pic_file,gt_file,dst):
    img = cv2.imread(pic_file)
    pic_name = os.path.basename(pic_file)
    attention_area = gt_file["attention_area"]["6"]
    xn = [float(x) for x in attention_area["xn"].replace('"', '').split(';')]
    yn = [float(y) for y in attention_area["yn"].replace('"', '').split(';')]
    tmp = []
    for i,temp in enumerate(xn):
        tmp.append([int(xn[i]),int(yn[i])])
    polygon_temp = np.array(tmp)
    cv2.polylines(img,[polygon_temp],isClosed=True,color=[0,255,0],thickness=2)
    if gt_file!={} and gt_file["obstacle"]!=[]:
        for each in gt_file["obstacle"]:
            for each2 in each['2d']:
                if int(each2["cameraId"])==6:            
                    x = int(each2["x"])
                    y = int(each2["y"]) 
                    w = int(each2["width"])
                    h = int(each2["height"])
                    x1 = x+w
                    y1 = y+h
                    cv2.rectangle(img, (x,y), (x1,y1),(0,0,255),2)
                    # perce_type = each2["type"]
                    # cv2.putText(img,perce_type,(x-20,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    print(os.path.join(dst,pic_name))
    cv2.imwrite(os.path.join(dst,pic_name),img)

for root,_,files in os.walk(pic):
    files = sorted(files,key=lambda x:int(x.split('.')[0]))
    for file_ in files:
        gt_json = file_.split('.')[0] + '.json'
        gt_json_data = utils.get_json_data(os.path.join(gt_json_path,gt_json))
        pic_path = os.path.join(root,file_.replace('.json','.jpg'))
        draw_gt(pic_path,gt_json_data,dst)




