import cv2
import pandas
import os
import shutil


start_frame = 18046  #要剪切的起始帧
end_frame = 18126 #要剪切的终止帧
video_path_far = '/home/chengjianlian/文档/mona/30KM/saved_data22/model_input_frame/front_far/front_far.mp4'  #输入要剪切的视频路径
video_path_near = '/home/chengjianlian/文档/mona/30KM/saved_data22/model_input_frame/front_near/front_near.mp4'  #输入要剪切的视频路径
name_far = 'front_far' #输入剪切出来的视频的名称
name_near = 'front_near' #输入剪切出来的视频的名称
timestamp_path = '/home/chengjianlian/文档/mona/30KM/saved_data22/model_input_frame/front_far/front_far.log' #视频时间搓文件路径
vehicle_state_path = '/home/chengjianlian/文档/mona/30KM/saved_data22/vehicle_status.txt' #vehicle state文件路径
casename = '左侧三轮车切入主车道不判断为cutin' #要case名称，以上的数据会移到该文件夹下面，方便整理


def cut_video(video_path,name,start_frame,end_frame):
    videoCapture = cv2.VideoCapture(video_path)
    fps = int(videoCapture.get(5))
    size = (int(videoCapture.get(3)),int(videoCapture.get(4)))
    videoWriter =cv2.VideoWriter('{}.mp4'.format(name),cv2.VideoWriter_fourcc('X','V','I','D'),fps,size)
    i = 0
    # 剪切视频
    while True:
        success,frame = videoCapture.read()
        if success:
            i += 1
            # print('i = ',i)
            if(i>=start_frame and i <= end_frame):
                videoWriter.write(frame)
            if i > end_frame:
                break
        else:
            print('end')   
            break 

os.makedirs(casename,exist_ok=True)
timestamp = pandas.read_csv(timestamp_path,sep=" ",header=None)
# cell =timestamp.iat[3,1]
# cell2 = timestamp.iat[6,1]
# print(cell,cell2)
# print(type(cell),type(cell2))
cut_timestamp_tmp = timestamp.loc[(timestamp[1]>=start_frame) & (timestamp[1]<=end_frame)]
cut_timestamp = cut_timestamp_tmp.copy()
cut_timestamp[1] = cut_timestamp[1].map(lambda x: int(x-start_frame))
cut_timestamp[3] = cut_timestamp[3].map(lambda x: int(x))

# print(cut_timestamp)
cut_timestamp.to_csv(casename +'/timestamp.txt',sep=' ',header=None,index=False)
vehicle_state = pandas.read_csv(vehicle_state_path,sep=" ",header=None)

cut_vehicle_state = vehicle_state.loc[(vehicle_state[23] >= start_frame) & (vehicle_state[23] <= end_frame)]
cut_vehicle_state[23] = cut_vehicle_state[23].map(lambda x: int(x-start_frame))
# print(cut_vehicle_state)
cut_vehicle_state.to_csv(casename +'/vehicle_state.txt',sep=' ',header=None,index=False)


cut_video(video_path_far,name_far,start_frame,end_frame)
cut_video(video_path_near,name_near,start_frame,end_frame)


shutil.move(name_far + str('.mp4'),os.path.join(casename,name_far + str('.mp4')))
shutil.move(name_near + str('.mp4'),os.path.join(casename,name_near + str('.mp4')))
