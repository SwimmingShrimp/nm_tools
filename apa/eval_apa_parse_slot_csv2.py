import os
import os.path as osp
import numpy as np
import cv2
import csv
import math
import pdb

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def non_maximum_suppression(pred_points):
    """Perform non-maxmum suppression on marking points."""
    suppressed = [False] * len(pred_points)
    for i in range(len(pred_points) - 1):
        for j in range(i + 1, len(pred_points)):
            i_x = pred_points[i][1][0]
            i_y = pred_points[i][1][1]
            j_x = pred_points[j][1][0]
            j_y = pred_points[j][1][1]
            # 0.03125 = 1 / 16
            if abs(j_x - i_x) < 0.03125 and abs(j_y - i_y) < 0.03125:
                idx = i if pred_points[i][0] < pred_points[j][0] else j
                suppressed[idx] = True
    if any(suppressed):
        unsupres_pred_points = []
        for i, supres in enumerate(suppressed):
            if not supres:
                unsupres_pred_points.append(pred_points[i])
        return unsupres_pred_points
    return pred_points

def get_predicted_points(prediction, thresh):
    """Get marking points from one predicted feature map."""
    predicted_points = []
    
    for i in range(prediction.shape[1]):
        for j in range(prediction.shape[2]):
            if prediction[0, i, j] >= thresh:
                # pdb.set_trace()
                xval = (j + prediction[1, i, j]) / prediction.shape[2]
                yval = (i + prediction[2, i, j]) / prediction.shape[1]
                if not (0.05 <= xval <= 1-0.05
                        and 0.05<= yval <= 1-0.05):
                    continue
                marking_point=[xval, yval]
                predicted_points.append((prediction[0, i, j],marking_point))
    return non_maximum_suppression(predicted_points)

def process(fpoint, fhm, fhm_max, foffset, fp1, fp2, fp3, fp4):
    keep = (fhm == fhm_max)
    clses = keep * fhm
    bboxes = []
    for cls, reg, point1, point2, point3, point4 in zip(clses, foffset, fp1, fp2, fp3, fp4):
        index = np.where(cls >= 0.5)
        score = np.array(cls[index])
        cat = np.array(index[0])
        ctx, cty = index[-1], index[-2]
        point1 = (point1-0.5)*2*50
        point2 = (point2-0.5)*2*50
        point3 = (point3-0.5)*2*50
        point4 = (point4-0.5)*2*50
        p1, p2 = point1[:, cty, ctx], point2[:, cty, ctx]
        p3, p4 = point3[:, cty, ctx], point4[:, cty, ctx]
        off_x, off_y = reg[0, cty, ctx], reg[1, cty, ctx]
        ctx = np.array(ctx) + np.array(off_x)
        cty = np.array(cty) + np.array(off_y)
        x1, y1 = ctx + p1[0], cty + p1[1]
        x2, y2 = ctx + p2[0], cty + p2[1]
        x3, y3 = ctx + p3[0], cty + p3[1]
        x4, y4 = ctx + p4[0], cty + p4[1]
        bbox = np.stack((cat, score, ctx,cty, x1, y1, x2, y2, x3, y3, x4, y4), axis=1).tolist()
        bbox = sorted(bbox, key=lambda x: x[1], reverse=True)
        bboxes.append(bbox)
    points = get_predicted_points(fpoint[0],0.7)
    return bboxes, points

def compute_angle(c, point1, point2):
    p1_p2 = point2 - point1
    pc = point1 + p1_p2 / 2
    num = np.dot(p1_p2, c-pc)
    denum = np.linalg.norm(p1_p2) * np.linalg.norm(c-pc)
    angle = math.acos(num / denum) * 180 / math.pi
    return angle

def compute_two_points(degree,type,c, point1, point2,model_input_shape):
    p1_p2 = point2 - point1
    p1_p2_norm = np.sqrt(p1_p2[0] ** 2 + p1_p2[1] ** 2)
    # print('The distance between point1 and point2:{}'.format(p1_p2_norm))
    if type==6 or type==7:
        depth = 125/900*model_input_shape
    else:
        depth = 320/900*model_input_shape
    p1_p2_unit = p1_p2 / p1_p2_norm
    rotate_matrix = np.array([[np.cos(degree / 180 * np.pi), np.sin(degree / 180 * np.pi)],
                              [-np.sin(degree / 180 * np.pi), np.cos(degree / 180 * np.pi)]])
    center_12=(point1+point2)/2
    direct_unit=(c-center_12)/np.linalg.norm(c-center_12)
    p2_p3_unit = np.dot(rotate_matrix, p1_p2_unit)
    if direct_unit.dot(p2_p3_unit)<30/180 * np.pi:
      p1_p2_unit = -p1_p2_unit
    p2_p3 = np.dot(rotate_matrix, p1_p2_unit) * depth
    point3 = point2 + p2_p3
    point4 = point1 + p2_p3
    return point3, point4

def show_result(image, save_path, bboxes, points,model_input_shape,img_shape):
    img_type = save_path.split('.')[-1]
    label_path = save_path.replace(img_type,'txt')
    label_file = open(label_path,'w') 
    for j, score, cx, cy, x1, y1, x2, y2, x3, y3, x4, y4 in bboxes[0]:
        if score > 0.3:
            # print(bboxes[0])
            cx = cx*img_shape/int(model_input_shape/4)
            cy = cy*img_shape/int(model_input_shape/4)
            c=np.array([cx,cy])
            p1 = x1*img_shape/int(model_input_shape/4),y1*img_shape/int(model_input_shape/4)
            p1 = np.array(p1)
            p2 = x2*img_shape/int(model_input_shape/4),y2*img_shape/int(model_input_shape/4)
            p2 = np.array(p2)
            p3_ = x3*img_shape/int(model_input_shape/4),y3*img_shape/int(model_input_shape/4)
            p3_ = np.array(p3_)
            p4_ = x4*img_shape/int(model_input_shape/4),y4*img_shape/int(model_input_shape/4)
            p4_ = np.array(p4_)
            cv2.circle(image,(int(cx),int(cy)),4,(0,0,0),4) #black
            cv2.circle(image,(int(p1[0]),int(p1[1])),4,(255,0,0),4) #blue
            cv2.circle(image,(int(p2[0]),int(p2[1])),4,(0,0,255),4) #red
            cv2.circle(image,(int(p3_[0]),int(p3_[1])),4,(0,255,0),4) #green
            cv2.circle(image,(int(p4_[0]),int(p4_[1])),4,(0,255,0),4) #green
            p1_best_dist=500
            p2_best_dist=500
            p1_best=np.zeros((2,))
            p2_best=np.zeros((2,))
            for p in points:
                p_x = img_shape * p[1][0] - 0.5
                p_y = img_shape * p[1][1] - 0.5
                p_ = np.array((p_x,p_y))
                dist_p1=np.linalg.norm(p1-p_)
                dist_p2=np.linalg.norm(p2-p_)
                if dist_p1<p1_best_dist:
                    p1_best_dist=dist_p1
                    p1_best = p_
                if dist_p2<p2_best_dist:
                    p2_best_dist=dist_p2
                    p2_best = p_
            if p1_best_dist<30:
                p1 = p1_best
            if p2_best_dist<30:
                p2 = p2_best
            if j==0 or j==1 or j==6 or j==7:
                angle = 90
            else:
                angle = compute_angle(c, p1, p2)
            # p3, p4 = compute_two_points(angle,j,c, p1, p2,model_input_shape)
            p3, p4 = p3_,p4_
            out_str = ','.join([str(j//2), str(p1[0]),str(p1[1]),str(p4[0]),str(p4[1]),str(p3[0]),str(p3[1]),str(p2[0]),str(p2[1]),str(int(j%2))]) +'\n'
            label_file.write(out_str)
            pts_show = np.array([p1, p2, p3, p4], np.int32)
            if j==1 or j==3 or j==5 or j==7:
                color=(255, 0, 0)
                cv2.putText(image,"Occupy slot",(int(c[0]),int(c[1])),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            else:
                color = (0, 255, 0)
                cv2.putText(image,"Empty slot",(int(c[0]),int(c[1])),cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            cv2.putText(image,"Conf: "+str(score),(int(c[0]),int(c[1])+30),cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
            cv2.polylines(image, [pts_show], True, color, 2)
    label_file.close()
    for confidence, marking_point in points:
        p0_x = int(img_shape * marking_point[0] - 0.5)
        p0_y = int(img_shape * marking_point[1] - 0.5)
        cv2.circle(image, (p0_x, p0_y),2, (0, 255, 255), 2)
        cv2.putText(image, str(confidence), (p0_x, p0_y),
                   cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
    cv2.imwrite(save_path, image)

def trans(v):
    return float(v[0].split(',')[0])

def read_csv(path):
    f = open(path, 'r')
    reader = list(csv.reader(f))
    lines = list(map(trans, reader))
    f.close()
    return lines

def fill_feature(arr, value, h, w):
    idx = 0
    for row in value:
        arr[:, idx // (h*w), idx // w % h, idx % w] = row
        idx += 1
    return arr

def gen_features(path_point, path_hm, path_max, path_offset, path_p1, path_p2, path_p3, path_p4,model_input_shape):
    # print(model_input_shape, model_input_shape/16, model_input_shape/16)
    fpoint = np.zeros((1, 3, int(model_input_shape/16), int(model_input_shape/16)))
    fhm = np.zeros((1, 8, int(model_input_shape/4), int(model_input_shape/4)))
    fhm_max = np.zeros((1, 8, int(model_input_shape/4), int(model_input_shape/4)))
    foffset = np.zeros((1, 2, int(model_input_shape/4), int(model_input_shape/4)))
    fp1 = np.zeros((1, 2, int(model_input_shape/4), int(model_input_shape/4)))
    fp2 = np.zeros((1, 2, int(model_input_shape/4), int(model_input_shape/4)))
    fp3 = np.zeros((1, 2, int(model_input_shape/4), int(model_input_shape/4)))
    fp4 = np.zeros((1, 2, int(model_input_shape/4), int(model_input_shape/4)))

    vpoint = read_csv(path_point)
    fpoint = fill_feature(fpoint, vpoint, int(model_input_shape/16), int(model_input_shape/16))
    vhm = read_csv(path_hm)
    fhm = fill_feature(fhm, vhm, int(model_input_shape/4), int(model_input_shape/4))
    vmax = read_csv(path_max)
    fhm_max = fill_feature(fhm_max, vmax, int(model_input_shape/4), int(model_input_shape/4))
    voffset = read_csv(path_offset)
    foffset = fill_feature(foffset, voffset, int(model_input_shape/4), int(model_input_shape/4))
    vp1 = read_csv(path_p1)
    fp1 = fill_feature(fp1, vp1, int(model_input_shape/4), int(model_input_shape/4))
    vp2 = read_csv(path_p2)
    fp2 = fill_feature(fp2, vp2, int(model_input_shape/4), int(model_input_shape/4))
    vp3 = read_csv(path_p3)
    fp3 = fill_feature(fp3, vp3, int(model_input_shape/4), int(model_input_shape/4))
    vp4 = read_csv(path_p4)
    fp4 = fill_feature(fp4, vp4, int(model_input_shape/4), int(model_input_shape/4))

    # return fpoint, fhm, fhm_max, foffset, fp1, fp2, fp3, fp4
    return sigmoid(fpoint), sigmoid(fhm), sigmoid(fhm_max), sigmoid(foffset), sigmoid(fp1), sigmoid(fp2), sigmoid(fp3), sigmoid(fp4)

def precess_img(imgpath,model_input_shape):
    save_path = imgpath.replace("parser_img/final_test_2","parser_img/r_test2_pre")
    print(imgpath)
    image = cv2.imread(imgpath)
    img_name = imgpath.split("/")[-1].split(".")[0]
    print(img_name)
    
    path_point = './csv/pic_{}.bmp_result_id_26.csv'.format(img_name)
    path_hm = './csv/pic_{}.bmp_result_id_45.csv'.format(img_name)
    path_max = './csv/pic_{}.bmp_result_id_46.csv'.format(img_name)
    path_offset = './csv/pic_{}.bmp_result_id_47.csv'.format(img_name)
    path_p1 = './csv/pic_{}.bmp_result_id_48.csv'.format(img_name)
    path_p2 = './csv/pic_{}.bmp_result_id_49.csv'.format(img_name)
    path_p3 = './csv/pic_{}.bmp_result_id_50.csv'.format(img_name)
    path_p4 = './csv/pic_{}.bmp_result_id_51.csv'.format(img_name)

    img_shape = image.shape[0]
    print("img shape:",img_shape)
    fpoint, fhm, fhm_max, foffset, fp1, fp2, fp3, fp4 = gen_features(path_point, path_hm, path_max, path_offset, path_p1, path_p2, path_p3, path_p4,model_input_shape)
    bboxes, points = process(fpoint, fhm, fhm_max, foffset, fp1, fp2, fp3, fp4)
    show_result(image, save_path, bboxes, points,model_input_shape,img_shape)
    
if __name__ == '__main__':
    image_ext = ['jpg', 'jpeg', 'png', 'webp','bmp']
    model_input_shape = 384
    root = "./parser_img/final_test_2/"
    for dirpath, dirnames, filenames in os.walk(root):
        for file in filenames:
            img_path = os.path.join(dirpath,file)
            file_type = file.split(".")[-1]
            if file_type in image_ext:
                try:
                    precess_img(img_path,model_input_shape)
                except Exception as e:
                    print(e)
                    continue
    

    

    
