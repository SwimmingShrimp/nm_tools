from distutils import command
from genericpath import exists
from re import S
import utils
import os
import config
import json
import pandas as pd
from datetime import datetime
import cv2
import shutil
from pathlib import Path as path

class Eval2DSide:
    def __init__(self, lable_path, perce_path, ori_pic_path):
        self.lable_path = lable_path
        self.perce_path = perce_path
        self.ori_pic_path = ori_pic_path
        self.iou = config.side_2d_config["iou"]
        self.proportion = config.side_2d_config["proportion"]
        self.topcut = config.side_2d_config["topcut"]
        self.obstacle_type = config.side_2d_config["obstacle_type"]
        self.enum_obstacle = config.side_2d_config["enum_obstacle"]
        self.subclass_type = config.side_2d_config["subclass_type"]
        self.class_subclass_type = config.side_2d_config["class_subclass_type"]
        self.str_time = (datetime.now()).strftime("%Y-%m-%d-%H-%M-%S")
        self.current_path = os.getcwd()
        self.excel_path = self.current_path + '/' + self.str_time + '/result'
        self.recall_error_path = self.current_path + '/' + self.str_time + '/side_2d_recall_error'
        self.precision_error_path = self.current_path + '/' + self.str_time+ '/side_2d_precision_error'
        os.makedirs(self.excel_path, exist_ok=True)
        os.makedirs(self.recall_error_path, exist_ok=True)
        os.makedirs(self.precision_error_path, exist_ok=True)

    def proc_json_data(self):
        '''
        标注json：所有的图片的标注结果都存放在一整个json文件中
        感知检测结果json：单张图片对应一个同名的json
        本方法主要是：将标注的整个json分成多个json,类似感知结果json
        '''
        self.perce_jsons_list = utils.get_json_list(self.perce_path)
        # self.lable_jsons_old_list = utils.get_json_list(self.lable_path)
        # lable_new_path = os.path.join(self.lable_path,'new')
        # if not os.path.exists(lable_new_path):
        #     os.makedirs(lable_new_path)
        # lable_json_data = utils.get_json_data(self.lable_jsons_old_list[0])
        # for lable_result in lable_json_data:
        #     if lable_result["task_vehicle"]==[]:
        #         continue
        #     lable_result_temp = lable_result
        #     lable_json_name = (lable_result["filename"])[:-4] + '.json'
        #     lable_new_json_path = lable_new_path + '/' + lable_json_name
        #     for perce_json in self.perce_jsons_list:
        #         perce_json_name = os.path.basename(perce_json)
        #         if lable_json_name == perce_json_name: 
        #             with open(lable_new_json_path,'w') as f:
        #                 json.dump(lable_result_temp,f,indent=4)
        #             break
        #     if not os.path.exists(lable_new_json_path):
        #         print('感知结果目录下不存在'+ lable_json_name + '文件，请检查！')
        # self.lable_jsons_list = utils.get_json_list(lable_new_path)
        self.lable_jsons_list = utils.get_json_list(self.lable_path)
    
    def match_lable_perce(self):
        '''
        根据所有的标注json文件，找到对应的感知结果json。在list中，同名的文件是一一对应的。
        '''
        self.perce_jsons_list_new = []
        for lable_json in  self.lable_jsons_list:
            lable_json_name = os.path.basename(lable_json)
            for perce_json in self.perce_jsons_list:
                perce_json_name = os.path.basename(perce_json)
                if lable_json_name==perce_json_name:
                    self.perce_jsons_list_new.append(perce_json)
        if len(self.lable_jsons_list)!=len(self.perce_jsons_list_new):
            print('感知json数量和标注json数量不一致，请检查！')

    def eval_2d_side_recall(self): 
        '''评测周视2d的recall指标'''       
        df = pd.DataFrame(columns=['KPI'] + self.obstacle_type)
        df.loc[0, 'KPI'] = '标注数量'
        df.loc[1, 'KPI'] = '检出数量'
        df.loc[2, 'KPI'] = '未检测数量'
        df.loc[3, 'KPI'] = '召回率'
        df.fillna(0, inplace=True) 
        recall_err_json = os.path.join(self.recall_error_path,'json')
        os.makedirs(recall_err_json, exist_ok=True)       
        for i in range(len(self.lable_jsons_list)):
            # 获取同一张图片的lable_json和perce_json的内容
            lable_json = self.lable_jsons_list[i]
            lable_json_name = os.path.basename(lable_json)
            lable_json_data = utils.get_json_data(lable_json)
            attention_area = lable_json_data["task_attention_area"][0]["tags"]
            perce_json = self.perce_jsons_list_new[i]
            perce_json_data = utils.get_json_data(perce_json)
            # 如果perce_json中检测结果为空，跳过
            if not perce_json_data:
                    continue
            # 获取所有的感知boxs列表
            perce_json_data_boxs = utils.get_perce_2d_boxs(perce_json_data)
            if perce_json_data_boxs == None:
                continue
            perce_box_list = []
            for perce_result in perce_json_data_boxs:
                perce_box = perce_result["uv_bbox2d"]
                perce_box_list.append(perce_box)
            recall_error_path = os.path.join(recall_err_json,lable_json_name)
            recall_error_list = []
            # 遍历所有的标注box，跟感知box比对
            for lable_tag in utils.get_lable_2d_boxs(lable_json_data):
                occluded_value = int(lable_tag["tags"]["occluded"])
                # 遮挡属性（occluded_value），1表示遮挡30%-90%，2表示遮挡90%以上，过滤掉
                if occluded_value!=0:
                    continue
                lable_type = lable_tag["tags"]["class"]
                # 如果标注类别不在评测的类别范围内，过滤掉
                if lable_type not in self.obstacle_type:
                    continue 
                lable_box,lx,ly = utils.get_lable_box(lable_tag)
                is_in_attentionArea = utils.judge_is_in_attentionArea(lx, ly, attention_area)
                # 如果不在attentionArea范围内，过滤掉
                if not is_in_attentionArea:
                    continue                  
                df.iloc[0, df.columns.get_loc(lable_type)] += 1
            
                iou_result = {}
                for j in range(len(perce_box_list)):
                    iou_result_value = utils.bb_intersection_over_union(lable_box,perce_box_list[j])
                    iou_result[j] = iou_result_value
                if iou_result=={}:
                    continue
                iou_max_item = max(iou_result.items(), key=lambda x: x[1])
                iou_max_value = iou_max_item[1]
                iou_max_id = iou_max_item[0]
                # iou大于0.5表示召回成功
                if iou_max_value >= self.iou:
                    df.iloc[1, df.columns.get_loc(lable_type)] += 1
                    del perce_box_list[iou_max_id]
                else:
                    recall_error_list.append(lable_box)
            if recall_error_list!=[]:
                print_json_comment = {}
                print_json_comment["lable_box"] = recall_error_list
                print_json_comment["perce_box"] = perce_box_list
                with open(recall_error_path,'w') as rf:
                    json.dump(print_json_comment,rf,indent=4)
        for type in self.obstacle_type:
            df.iloc[2,df.columns.get_loc(type)] = df.iloc[0,df.columns.get_loc(type)] -df.iloc[1,df.columns.get_loc(type)]
            df.iloc[3,df.columns.get_loc(type)] = 0 if df.iloc[1,df.columns.get_loc(type)]==0 else round(df.iloc[1,df.columns.get_loc(type)]*100/df.iloc[0,df.columns.get_loc(type)],3)
        df.to_excel(self.excel_path + '/' + self.str_time + '_recall.xlsx')
        print(df)

    def eval_2d_side_precision(self):
        '''评测周视2d的precision指标'''
        df = pd.DataFrame(columns=['KPI'] + self.obstacle_type)
        df.loc[0, 'KPI'] = '检测类别正确数量'
        df.loc[1, 'KPI'] = '检测类别错误数量'
        df.loc[2, 'KPI'] = '误检数量'
        df.loc[3, 'KPI'] = '检测出的总数量'
        df.loc[4, 'KPI'] = '检出精确率'
        df.loc[5, 'KPI'] = '类别精确率'
        df.fillna(0, inplace=True)
        self.precision_type_err_json = os.path.join(self.precision_error_path,'type_err_json')
        self.precision_misc_err_json = os.path.join(self.precision_error_path,'misc_err_json')
        os.makedirs(self.precision_type_err_json, exist_ok=True)
        os.makedirs(self.precision_misc_err_json, exist_ok=True)
        for i in range(len(self.lable_jsons_list)):
            # 获取lable_json和perce_json的内容
            lable_json = self.lable_jsons_list[i]
            lable_json_name = os.path.basename(lable_json)
            lable_json_data = utils.get_json_data(lable_json)
            attention_area = lable_json_data["task_attention_area"][0]["tags"]
            perce_json = self.perce_jsons_list_new[i]
            perce_json_data = utils.get_json_data(perce_json)
            # 过滤掉，一张图片，没有任何感知结果的场景
            if not perce_json_data:
                    continue
            perce_box_list = []
            precision_type_err_path = os.path.join(self.precision_type_err_json,lable_json_name)
            precision_misc_err_path = os.path.join(self.precision_misc_err_json,lable_json_name)
            precision_type_error_list = []
            precision_misc_error_list = []
            perce_box_type_list = []
            perce_json_data_boxs = utils.get_perce_2d_boxs(perce_json_data)
            if perce_json_data_boxs==None:
                continue
            for perce_result in perce_json_data_boxs:
                perce_box = perce_result["uv_bbox2d"]
                perce_box_type = perce_result["obstacle_type"]
                perce_box_list.append(perce_box)
                perce_box_type_list.append(perce_box_type)
            for lable_tag in utils.get_lable_2d_boxs(lable_json_data):
                occluded_value = int(lable_tag["tags"]["occluded"])
                if occluded_value!=0:
                    continue
                lable_type = lable_tag["tags"]["class"]
                if lable_type not in self.obstacle_type:
                    continue 
                lable_box,lx,ly = utils.get_lable_box(lable_tag)
                is_in_attentionArea = utils.judge_is_in_attentionArea(lx, ly, attention_area)
                if not is_in_attentionArea:
                    continue                              
                iou_result = {}
                for j in range(len(perce_box_list)):
                    iou_result_value = utils.bb_intersection_over_union(lable_box,perce_box_list[j])
                    iou_result[j] = iou_result_value
                if iou_result=={}:
                    continue
                iou_max_item = max(iou_result.items(), key=lambda x: x[1])
                iou_max_value = iou_max_item[1]
                iou_max_id = iou_max_item[0]
                if iou_max_value >= self.iou:
                    perce_type_value = perce_json_data_boxs[iou_max_id]["obstacle_type"]
                    perce_type = self.enum_obstacle[perce_type_value]
                    print_json_comment={}
                    if lable_type==perce_type:
                        df.iloc[0, df.columns.get_loc(lable_type)] += 1
                        del perce_box_list[iou_max_id]
                        del perce_box_type_list[iou_max_id]
                    else:
                        df.iloc[1, df.columns.get_loc(lable_type)] += 1
                        print_json_comment["lable_type"] = lable_type
                        print_json_comment["perce_type"] = perce_type
                        print_json_comment["lable_box"] = lable_box
                        print_json_comment["perce_box"] = perce_box_list[iou_max_id]
                        precision_type_error_list.append(print_json_comment)
            if precision_type_error_list!=[]:
                with open(precision_type_err_path,'w') as pf:
                    json.dump(precision_type_error_list,pf,indent=4)
            if perce_box_list != []:
                for j in range(len(perce_box_list)):
                    precision_misc_error_comment = {}
                    perce_box_type_value = perce_box_type_list[j]
                    precision_misc_error_comment["perce_type"] = self.enum_obstacle[perce_box_type_value]
                    precision_misc_error_comment["perce_box"] = perce_box_list[j]
                    precision_misc_error_list.append(precision_misc_error_comment)
                    df.iloc[2, df.columns.get_loc(self.enum_obstacle[perce_box_type_value])] += 1
                with open(precision_misc_err_path, 'w') as pme:
                    json.dump(precision_misc_error_list, pme, indent=4)
                precision_misc_error_list.extend(perce_box_list)
        for type in self.obstacle_type:
            df.iloc[3,df.columns.get_loc(type)] = df.iloc[0,df.columns.get_loc(type)] + df.iloc[1,df.columns.get_loc(type)] + df.iloc[2,df.columns.get_loc(type)]
            df.iloc[4,df.columns.get_loc(type)] = 0 if df.iloc[3,df.columns.get_loc(type)]==0 else round((df.iloc[0,df.columns.get_loc(type)] + df.iloc[1,df.columns.get_loc(type)])*100/df.iloc[3,df.columns.get_loc(type)],3)
            df.iloc[5,df.columns.get_loc(type)] = 0 if df.iloc[0,df.columns.get_loc(type)]==0 else round(df.iloc[0,df.columns.get_loc(type)]*100/(df.iloc[0,df.columns.get_loc(type)] + df.iloc[1,df.columns.get_loc(type)]),3)
        df.to_excel(self.excel_path + '/' + self.str_time + '_precision.xlsx')
        print(df)
    
    def get_oripic_depend_errorjson(self,err_json,ori_pic):
        '''根据已有报错的json文件名，找到对应的原始图片'''
        self.err_oripic = os.path.join(err_json,'oripic')
        if os.path.exists(self.err_oripic):
            shutil.rmtree(self.err_oripic)
        os.makedirs(self.err_oripic)
        pngname_list = []
        for root,_,files in os.walk(err_json):
            for file_ in files:
                png_name = file_[:-4] + 'png'
                pngname_list.append(png_name)
        for root,_,files in os.walk(ori_pic):
            for file_ in files:
                if file_ in pngname_list:
                    oripic_path = os.path.join(root,file_)
                    command = 'cp {} {}'.format(oripic_path,self.err_oripic)
                    os.system(command)
    
    def draw_recall_pic(self):
        '''
        绿色是标注结果，蓝色是感知结果
        '''
        Eval2DSide.get_oripic_depend_errorjson(self, self.recall_error_path,self.ori_pic_path)
        err_pic = os.path.join(self.recall_error_path,'errpic')
        if os.path.exists(err_pic):
            shutil.rmtree(err_pic)
        os.makedirs(err_pic)  
        for root,_,files in os.walk(os.path.join(self.recall_error_path,'json')):
            for file_ in files:
                json_path = os.path.join(root,file_)
                json_data = utils.get_json_data(json_path)
                lable_boxs = json_data["lable_box"]
                perce_boxs = json_data["perce_box"]
                img_name = file_[:-4] + 'png'
                img_data = cv2.imread(os.path.join(self.err_oripic,img_name))
                img_dstpath = os.path.join(err_pic,img_name)
                for lable_box in lable_boxs:
                    x,y,x1,y1 = utils.get_box_point(lable_box)                
                    cv2.rectangle(img_data,(x,y),(x1,y1),(0,255,0),2)
                for perce_box in perce_boxs:
                    x,y,x1,y1 = utils.get_box_point(perce_box)                
                    cv2.rectangle(img_data,(x,y),(x1,y1),(255,0,0),2)
                cv2.imwrite(img_dstpath, img_data)

    def draw_precision_pic(self):
            Eval2DSide.get_oripic_depend_errorjson(self, self.precision_type_err_json,self.ori_pic_path)
            Eval2DSide.get_oripic_depend_errorjson(self, self.precision_misc_err_json,self.ori_pic_path)
            precision_type_err_pic = os.path.join(self.precision_type_err_json,'type_err_pic')
            precision_misc_err_pic = os.path.join(self.precision_misc_err_json,'misc_err_pic')
            os.makedirs(precision_type_err_pic, exists_ok=True)
            os.makedirs(precision_misc_err_pic, exists_ok=True)
            for root,_,files in os.walk(os.path.join(self.precision_error_path,'type_err_json')):
                for file_ in files:
                    json_path = os.path.join(root,file_)
                    json_data = utils.get_json_data(json_path)
                    img_name = file_[:-4] + 'png'
                    img_data = cv2.imread(os.path.join(self.err_oripic,img_name))
                    img_dstpath = os.path.join(precision_type_err_pic,img_name)
                    for json_data_ in json_data:
                        lable_type = json_data_["lable_type"]
                        perce_type = json_data_["perce_type"]
                        lable_box = json_data_["lable_box"]
                        perce_box = json_data_["perce_box"]
                        x,y,x1,y1 = utils.get_box_point(lable_box)
                        x2,y2,x3,y3 = utils.get_box_point(perce_box)               
                        cv2.rectangle(img_data,(x,y),(x1,y1),(0,255,0),1)
                        cv2.rectangle(img_data,(x2,y2),(x3,y3),(0,0,255),1)
                        cv2.putText(img_data,lable_type,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)
                        cv2.putText(img_data,perce_type,(x2,y3),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
                    cv2.imwrite(img_dstpath, img_data)

            for root,_,files in os.walk(os.path.join(self.precision_error_path,'misc_err_json')):
                for file_ in files:
                    json_path = os.path.join(root,file_)
                    json_data = utils.get_json_data(json_path)
                    img_name = file_[:-4] + 'png'
                    img_data = cv2.imread(os.path.join(self.err_oripic,img_name))
                    img_dstpath = os.path.join(precision_misc_err_pic,img_name)
                    for json_data_ in json_data:
                        perce_type = json_data_["perce_type"]
                        perce_box = json_data_["perce_box"]
                        x2,y2,x3,y3 = utils.get_box_point(perce_box)               
                        cv2.rectangle(img_data,(x2,y2),(x3,y3),(0,0,255),1)
                    cv2.imwrite(img_dstpath, img_data) 

            
    def eval_subsclass_side_recall(self):
        '''评测周视2d细分类的recall指标'''       
        df = pd.DataFrame(columns=['KPI'] + self.class_subclass_type)
        df.loc[0, 'KPI'] = '标注数量'
        df.loc[1, 'KPI'] = '检出数量'
        df.loc[2, 'KPI'] = '未检测数量'
        df.loc[3, 'KPI'] = '召回率'
        df.fillna(0, inplace=True) 
        recall_err_json = os.path.join(self.recall_error_path,'json')
        if os.path.exists(recall_err_json):
            shutil.rmtree(recall_err_json)
        os.makedirs(recall_err_json)       
        for i in range(len(self.lable_jsons_list)):
            lable_json = self.lable_jsons_list[i]
            lable_json_name = os.path.basename(lable_json)
            lable_json_data = utils.get_json_data(lable_json)
            attention_area = lable_json_data["task_attention_area"][0]["tags"]
            perce_json = self.perce_jsons_list_new[i]
            perce_json_data = utils.get_json_data(perce_json)
            if not perce_json_data:
                    continue
            perce_json_data_boxs = utils.get_perce_2d_boxs(perce_json_data)
            perce_box_list = []
            for perce_result in perce_json_data_boxs:
                perce_box = perce_result["uv_bbox2d"]
                perce_box_list.append(perce_box)
            recall_error_path = os.path.join(recall_err_json,lable_json_name)
            recall_error_list = []
            for lable_tag in utils.get_lable_2d_boxs(lable_json_data):
                occluded_value = int(lable_tag["tags"]["occluded"])
                if occluded_value!=0:
                    continue
                lable_type = lable_tag["tags"]["class"]
                lable_sub_type = lable_tag["tags"]["subclass"]
                if lable_type not in self.subclass_type:
                    continue 
                lable_box,lx,ly = utils.get_lable_box(lable_tag)
                is_in_attentionArea = utils.judge_is_in_attentionArea(lx, ly, attention_area)
                if not is_in_attentionArea:
                    continue                  
                df.iloc[0, df.columns.get_loc(lable_type + '_' + lable_sub_type)] += 1
            
                iou_result = {}
                for j in range(len(perce_box_list)):
                    iou_result_value = utils.bb_intersection_over_union(lable_box,perce_box_list[j])
                    iou_result[j] = iou_result_value
                if iou_result=={}:
                    continue
                iou_max_item = max(iou_result.items(), key=lambda x: x[1])
                iou_max_value = iou_max_item[1]
                iou_max_id = iou_max_item[0]
                if iou_max_value >= self.iou:
                    df.iloc[1, df.columns.get_loc(lable_type + '_' + lable_sub_type)] += 1
                    del perce_box_list[iou_max_id]
                else:
                    recall_error_list.append(lable_box)
            if recall_error_list!=[]:
                print_json_comment = {}
                print_json_comment["lable_box"] = recall_error_list
                print_json_comment["perce_box"] = perce_box_list
                print(print_json_comment)
                with open(recall_error_path,'w') as rf:
                    json.dump(print_json_comment,rf,indent=4)
        for type in self.obstacle_type:
            df.iloc[2,df.columns.get_loc(type)] = df.iloc[0,df.columns.get_loc(type)] -df.iloc[1,df.columns.get_loc(type)]
            df.iloc[3,df.columns.get_loc(type)] = 0 if df.iloc[1,df.columns.get_loc(type)]==0 else round(df.iloc[1,df.columns.get_loc(type)]*100/df.iloc[0,df.columns.get_loc(type)],3)
        df.to_excel(self.excel_path + '/' + self.str_time + '_recall.xlsx')
        print(df)


    def eval_subsclass_side_precision(self):
        pass
