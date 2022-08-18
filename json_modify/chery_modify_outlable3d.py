import os
import sys
sys.path.append('..')
import utils
import config

json_src = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/1_json/chery/3d_outlable_ori'
json_dst = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/1_json/chery/3d_lable_merge'
json_dst2 = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/1_json/chery/3d_lable_merge2'
os.makedirs(json_dst,exist_ok=True)
os.makedirs(json_dst2,exist_ok=True)

'''
将外部标注的数据，挑选内部需要的内容，转成新的格式
-----3d-----
dimension,x,y,z:长宽高
orientation，x,y,z：绕着对应的轴的朝向，pitch-俯仰角,yaw-航向角,roll-翻滚角
position，x,y,z：自车坐标系下的位置，x为纵向距离，y为横向左右距离，z不用管
-----2d-----
x,y:左上角点
w,h:宽，高
'''
def change_json():
    for root, _, files in os.walk(json_src):
        for file_ in files:
            json_data = utils.get_json_data(os.path.join(root,file_))
            data_3d = json_data["frames"][0]["items"]
            data_2d = json_data["frames"][0]["images"][0]["items"]
            json_3d = []
            for temp_3d in data_3d:
                type_3d = (temp_3d["category"]).lower()
                # type_value_3d = config.front_config["enum_obstacle2"][type_3d]
                dimension = temp_3d["dimension"]
                orientation = temp_3d["rotation"]
                position = temp_3d["position"]
                id = temp_3d["id"]
                match_2d_data = [x for x in data_2d if x["id"]==id]
                box_2d = {
                    "x":match_2d_data[0]["position"]["x"],
                    "y":match_2d_data[0]["position"]["y"],
                    "w":match_2d_data[0]["dimension"]["x"],
                    "h":match_2d_data[0]["dimension"]["y"]
                }
                temp = {
                    "id":id,
                    "type":type_3d,
                    "dimension":dimension,
                    "orientation":orientation,
                    "position":position,
                    "box_2d":box_2d
                }
                json_3d.append(temp)
            utils.write_json_data(os.path.join(json_dst,file_),json_3d)

'''根据id信息，算出速度和加速度'''
def calc_vel_accel():
    runtime = 6
    for root, _, files in os.walk(json_dst):
        files.sort(key=lambda x:int(x.split('_')[-1].split('.')[0]))
        for i in range(len(files)-1):
            json_data1 = utils.get_json_data(os.path.join(root,files[i]))
            json_data2 = utils.get_json_data(os.path.join(root,files[i+1]))
            if int(files[i].split('.')[0])+1 == int(files[i+1].split('.')[0]):
                if  int(files[i].split('.')[0])-1 == int(files[i-1].split('.')[0]):
                    for temp1 in json_data1:
                        temp2 = [x for x in json_data2 if x["id"]==temp1["id"]]
                        if not temp2:
                            continue
                        else:
                            temp2 = temp2[0]
                        temp2["velocity"]={
                            "x": round((temp1["position"]["x"]-temp2["position"]["x"]) / 0.2,3),
                            "y": round((temp1["position"]["y"]-temp2["position"]["y"]) / 0.2,3),
                            "z": round((temp1["position"]["z"]-temp2["position"]["z"]) / 0.2,3),
                        }
                        temp2["accel"]={
                            "x": round((temp1["position"]["x"]-temp2["position"]["x"]) / (0.2*0.2),3),
                            "y": round((temp1["position"]["y"]-temp2["position"]["y"]) / (0.2*0.2),3),
                            "z": round((temp1["position"]["z"]-temp2["position"]["z"]) / (0.2*0.2),3),
                        }
                    utils.write_json_data(os.path.join(json_dst2,files[i+1]),json_data2)   
                else:
                    for temp in json_data1:
                        temp['velocity']= {"x": -1000, "y": -1000, "z": -1000}
                        temp['accel']= {"x": -1000, "y": -1000, "z": -1000}
                    for temp1 in json_data1:
                        temp2 = [x for x in json_data2 if x["id"]==temp1["id"]]
                        if not temp2:
                            continue
                        else:
                            temp2 = temp2[0]
                        temp2["velocity"]={
                            "x": round((temp1["position"]["x"]-temp2["position"]["x"]) / 0.2,3),
                            "y": round((temp1["position"]["y"]-temp2["position"]["y"]) / 0.2,3),
                            "z": round((temp1["position"]["z"]-temp2["position"]["z"]) / 0.2,3),
                        }
                        temp2["accel"]={
                            "x": round((temp1["position"]["x"]-temp2["position"]["x"]) / (0.2*0.2),3),
                            "y": round((temp1["position"]["y"]-temp2["position"]["y"]) / (0.2*0.2),3),
                            "z": round((temp1["position"]["z"]-temp2["position"]["z"]) / (0.2*0.2),3),
                        }
                    utils.write_json_data(os.path.join(json_dst2,files[i]),json_data1)
                    utils.write_json_data(os.path.join(json_dst2,files[i+1]),json_data2)
        

def main():
    change_json()
    calc_vel_accel()


if __name__=="__main__":
    main()
