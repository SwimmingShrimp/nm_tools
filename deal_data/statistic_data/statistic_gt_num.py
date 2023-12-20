import os
# import sys
# sys.path.append('../..')
import utils
import argparse
import pandas as pd



enumerate_moving_type = ['car','truck','bus','pedestrian','motorcycle','bicycle','tricycle','kid']
enumerate_static_type = ['cone','barrier', 'barrel']
enumerate_tl_ignore_type = ["uncertain","unknown","pedestrian","bicycle",'None']
enumerate_tsr_ignore_type = ["uncertain","ignore","future","weight_limit","speed_limit15","speed_limit25","speed_limit35","speed_limit45",
                    "speed_limit55","speed_limit65","speed_limit75","speed_limit85","speed_limit95","speed_limit105","speed_limit115"]
enumerate_tl_type = ['circle','straight_arrow','left_arrow','right_arrow','uturn_arrow','straight_left_arrow','straight_right_arrow']
enumerate_tl_clor = ['red','yellow','green']
enumerate_tsr_type = ['warning_kid','warning_pedestrian','warning_construction','left_road_merge','no_entry','no_stopping',
'no_waiting','no_parking','stop','no_motor_entry','no_left','no_right','no_straight','no_turn','no_overtaking',
'allow_overtaking','change_route_left','change_route_right','induction_left','induction_right','left_road_closure',
'right_road_closure','middle_road_closure','road_closure',"speed_limit5","speed_limit10","speed_limit20","speed_limit30",
"speed_limit40","speed_limit50","speed_limit60","speed_limit70","speed_limit80",
"speed_limit90","speed_limit100","speed_limit110","speed_limit120",'right_road_merge']

def statistic_obstacle_num(json_path,statistic_type):
    single_data = []
    gt_json_data = utils.get_json_data(json_path)
    front_far_attention_area = gt_json_data["attention_area"][str(0)]
    front_near_attention_area = gt_json_data["attention_area"][str(1)]
    side_lf_attention_area = gt_json_data["attention_area"][str(3)]
    side_lr_attention_area = gt_json_data["attention_area"][str(2)]
    side_rf_attention_area = gt_json_data["attention_area"][str(4)]
    side_rr_attention_area = gt_json_data["attention_area"][str(5)]
    back_attention_area = gt_json_data["attention_area"][str(6)]
    obstacle_value = "obstacle"
    if gt_json_data[obstacle_value]:
        for temp1 in gt_json_data[obstacle_value]:
            for temp2 in temp1["2d"]:
                obstacle_type = temp2["type"]
                camera_id = temp2["cameraId"]
                is_not_occluded_value = 1
                occluded = temp2["occluded"]
                if int(occluded)!=0:
                    is_not_occluded_value = 0
                x = temp2["x"]
                y = temp2["y"]
                w = temp2["width"]
                h = temp2["height"]
                center_x = x + w/2
                center_y = y + h/2
                is_attentionarea_value =1
                if camera_id==0:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, front_far_attention_area)
                elif camera_id==1:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, front_near_attention_area)
                elif camera_id==2:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, side_lr_attention_area)
                elif camera_id==3:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, side_lf_attention_area)
                elif camera_id==4:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, side_rf_attention_area)
                elif camera_id==5:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, side_rr_attention_area)
                elif camera_id==6:
                    is_in_attentionArea = utils.judge_is_in_attentionArea(center_x, center_y, back_attention_area)
                else:
                    print('camear_id是{}，请检查'.format(camera_id))
                if not is_in_attentionArea:
                    is_attentionarea_value =0

                is_eval_type_value = 1
                if statistic_type=="moving":
                    if obstacle_type not in enumerate_moving_type:
                        is_eval_type_value=0
                elif statistic_type=="static":
                    if obstacle_type not in enumerate_static_type:
                        is_eval_type_value=0

                is_not_cut_value =1
                if statistic_type == 'moving':
                    if camera_id ==0 and y+h>=(2160-540):
                        is_not_cut_value = 0
                elif statistic_type == 'static':
                    if camera_id==1 or camera_id==0:
                        if y+h>=(2160-540):
                            is_not_cut_value = 0

                single_data.append([obstacle_type,is_attentionarea_value,is_eval_type_value,is_not_occluded_value,is_not_cut_value])
    return single_data

def statistic_tsr_num(json_path):
    single_data = []
    gt_json_data = utils.get_json_data(json_path)
    obstacle_value = "obstacle_tsr"
    if gt_json_data[obstacle_value]:
        for temp1 in gt_json_data[obstacle_value]:
            for temp2 in temp1["2d"]:
                tsr_type = temp2["type"]
                if temp2["is_min"]==1:
                    tsr_type = tsr_type + '_min'
                if temp2["is_end"]==1:
                    tsr_type = tsr_type + '_end'
                if temp2["is_led"]==1:
                    tsr_type = tsr_type + '_led'
                if temp2["is_ring"]==1:
                    tsr_type = tsr_type + '_ring' 

                x = temp2["x"]
                y = temp2["y"]
                w = temp2["width"]
                h = temp2["height"]
                camera_id = temp2["cameraId"]
                is_eval_type_value = 1
                if tsr_type in enumerate_tsr_ignore_type:
                    is_eval_type_value=0
                is_not_cut_value =1
                if (camera_id==0 and y<=40) or (camera_id==1 and y<=180):
                    is_not_cut_value = 0
                if camera_id in [2,3,4,5] and y<=120:
                    is_not_cut_value = 0
                if camera_id ==6 and y<=240:
                    is_not_cut_value = 0
            single_data.append([tsr_type,is_eval_type_value,is_not_cut_value])
    return single_data

def statistic_tl_num(json_path):
    single_data = []
    gt_json_data = utils.get_json_data(json_path)
    obstacle_value = "obstacle_tl"
    if gt_json_data[obstacle_value]:
        for temp1 in gt_json_data[obstacle_value]:
            for temp2 in temp1["2d"]:
                tl_shape = temp2["shape"]
                tl_color = temp2["color"]
                x = temp2["x"]
                y = temp2["y"]
                w = temp2["width"]
                h = temp2["height"]
                camera_id = temp2["cameraId"]
                is_eval_shape_type_value = 1
                is_eval_color_type_value = 1
                if tl_shape not in enumerate_tl_type:
                    is_eval_shape_type_value=0
                if tl_color not in enumerate_tl_clor:
                    is_eval_color_type_value=0
                is_not_cut_value =1
                if (camera_id==0 and y<=40) or (camera_id==1 and y<=180):
                    is_not_cut_value = 0
                if camera_id in [2,3,4,5] and y<=120:
                    is_not_cut_value = 0
                if camera_id ==6 and y<=240:
                    is_not_cut_value = 0
            single_data.append([tl_shape,tl_color,is_eval_shape_type_value,is_eval_color_type_value,is_not_cut_value])
    return single_data


def analyse_obstacle_table(table_path):
    df = pd.read_excel(table_path,sheet_name='全部数据',index_col=0)
    df['标注总数量']=1
    df['在attention_area范围内']=1
    df['在attention_area范围内且是需要评测类别']=1
    df['在attention_area范围内且是需要评测类别且未被遮挡']=1
    df['有效评测数量']=1
    data = df.groupby(['障碍物类别']).agg({'标注总数量':'sum'})
    data1 = df[(df["是否在attention范围内"]==1)]
    data2 = data1.groupby(['障碍物类别']).agg({'在attention_area范围内':'sum'})
    data3 = df[(df["是否在attention范围内"]==1) & (df["是否是想要评估的类别"]==1)]
    data4 = data3.groupby(['障碍物类别']).agg({'在attention_area范围内且是需要评测类别':'sum'})
    data5 = df[(df["是否在attention范围内"]==1) & (df["是否是想要评估的类别"]==1)& (df["是否被遮挡"]==1)]
    data6 = data5.groupby(['障碍物类别']).agg({'在attention_area范围内且是需要评测类别且未被遮挡':'sum'})
    data7 = df[(df["是否在attention范围内"]==1) & (df["是否是想要评估的类别"]==1)& (df["是否被遮挡"]==1)& (df["是否被裁切过滤"]==1)]
    data8 = data7.groupby(['障碍物类别']).agg({'有效评测数量':'sum'})
    all_data = pd.concat([data,data2,data4,data6,data8],axis=1)
    with pd.ExcelWriter(table_path, mode='a',engine="openpyxl") as writer:
        all_data.to_excel(writer, sheet_name='分类别数据量统计')

def analyse_tsr_table(table_path):
    df = pd.read_excel(table_path,sheet_name='全部数据',index_col=0)
    df['标注总数量']=1
    df['有效评测数量']=1
    data = df.groupby(['障碍物类别']).agg({'标注总数量':'sum'})
    data1 = df[(df["是否是想要评估的类别"]==1) & (df["是否被裁切过滤"]==1)]
    data2 = data1.groupby(['障碍物类别']).agg({'有效评测数量':'sum'})
    all_data = pd.concat([data,data2],axis=1)
    with pd.ExcelWriter(table_path, mode='a',engine="openpyxl") as writer:
        all_data.to_excel(writer, sheet_name='分类别数据量统计')

def analyse_tl_table(table_path):
    df = pd.read_excel(table_path,sheet_name='全部数据',index_col=0)
    df['标注总数量']=1
    df['有效评测数量']=1
    data = df.groupby(['交通灯形状']).agg({'标注总数量':'sum'})
    data1 = df[(df["是否可评测的交通灯形状"]==1) & (df["是否被裁切过滤"]==1)]
    data2 = data1.groupby(['交通灯形状']).agg({'有效评测数量':'sum'})
    all_data = pd.concat([data,data2],axis=1)
    with pd.ExcelWriter(table_path, mode='a',engine="openpyxl") as writer:
        all_data.to_excel(writer, sheet_name='根据交通灯形状统计')
    data4 = df.groupby(['交通灯颜色']).agg({'标注总数量':'sum'})
    data5 = df[(df["是否可评测的交通灯颜色"]==1) & (df["是否被裁切过滤"]==1)]
    data6 = data5.groupby(['交通灯颜色']).agg({'有效评测数量':'sum'})
    all_data2 = pd.concat([data4,data6],axis=1)
    with pd.ExcelWriter(table_path, mode='a',engine="openpyxl") as writer:
        all_data2.to_excel(writer, sheet_name='根据交通灯颜色统计')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('json_path',type=str)
    parser.add_argument('statistic_type',type=str)
    parser.add_argument('dst',type=str)
    args = parser.parse_args()
    json_path = args.json_path
    statistic_type = args.statistic_type
    dst = args.dst
    all_data = []
    if statistic_type in ['moving','static']:
        for root,_,files in os.walk(json_path):
            files = sorted(files,key=lambda x:int(x.split('.')[0]))
            for file_ in files:
                all_data.extend(statistic_obstacle_num(os.path.join(root,file_),statistic_type))
        df = pd.DataFrame(all_data,columns=['障碍物类别','是否在attention范围内','是否是想要评估的类别','是否被遮挡','是否被裁切过滤'])
        df.to_excel('{}/{}{}.xlsx'.format(dst,statistic_type,56),sheet_name='全部数据')
        analyse_obstacle_table('{}/{}{}.xlsx'.format(dst,statistic_type,56))
    elif statistic_type=='tsr':
        for root,_,files in os.walk(json_path):
            files = sorted(files,key=lambda x:int(x.split('.')[0]))
            for file_ in files:
                all_data.extend(statistic_tsr_num(os.path.join(root,file_)))
        df = pd.DataFrame(all_data,columns=['障碍物类别','是否是想要评估的类别','是否被裁切过滤'])
        df.to_excel('{}/{}.xlsx'.format(dst,statistic_type),sheet_name='全部数据')
        analyse_tsr_table('{}/{}.xlsx'.format(dst,statistic_type))
    elif statistic_type=='tl':
        for root,_,files in os.walk(json_path):
            files = sorted(files,key=lambda x:int(x.split('.')[0]))
            for file_ in files:
                all_data.extend(statistic_tl_num(os.path.join(root,file_)))
        df = pd.DataFrame(all_data,columns=['交通灯形状','交通灯颜色','是否可评测的交通灯形状','是否可评测的交通灯颜色','是否被裁切过滤'])
        df.to_excel('{}/{}.xlsx'.format(dst,statistic_type),sheet_name='全部数据')
        analyse_tl_table('{}/{}.xlsx'.format(dst,statistic_type))

    
    



