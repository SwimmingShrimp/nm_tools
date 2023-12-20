import rosbag
import sys
import os
import numpy as np

# cameras=["front_far","front_near","side_left_front","side_lefr_rear","side_right_front","side_right_rear","back_middle"]
wanted_cameras=["back_middle"]
wanted_pic_topics=[]
wanted_pic_counter={}
for i in range(0,len(wanted_cameras)):
    wanted_pic_topics.append("/perception/"+wanted_cameras[i]+"_image")
    wanted_pic_counter[wanted_cameras[i]]=0


def Usage():
    print("./ros_parse_pic.py <bag_path> <pic_path>")

def MakeAllDir(pic_path):
    if not os.path.exists(pic_path):
        os.mkdir(pic_path)
    for i in range(0, len(wanted_cameras)):
        sub_dir=pic_path+"/" +wanted_cameras[i]
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)

def RosBagParsePic(perception_bag,pic_path):
    try:
        perception = rosbag.Bag(perception_bag, "r")
    except Exception as e:
        print(e)
        return
    MakeAllDir(pic_path)
    for topic, msg, t in perception.read_messages(wanted_pic_topics):
        #/perception/${camera}_image
        camera = topic[12:-6]
        pic_name = pic_path+"/"+camera+"/"+str(wanted_pic_counter[camera])+".jpg"
        wanted_pic_counter[camera] = wanted_pic_counter[camera] +1
        #保存到磁盘
        int8_array = np.array(msg.data, dtype=np.int8)
        # uint8_array = np.reshape(np.frombuffer(int8_array.tobytes(), dtype=np.uint8), (-1, 1))
        f=open(pic_name,"wb")
        f.write(int8_array.tobytes())
        f.close()
        print("write "+pic_name)



# python ./ros_parse_pic.py <bag_path>
if __name__ == '__main__':
    if len(sys.argv) < 2:
        Usage()
        exit(-1)
    perception_bag = sys.argv[1]
    pic_path = sys.argv[2]
    RosBagParsePic(perception_bag,pic_path)