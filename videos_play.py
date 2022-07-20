# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from argparse import ArgumentParser
import csv

def nothing(x):
    pass

def cv2showimgs(scale, imglist, order):
    
    allimgs = imglist.copy()
    for i, img in enumerate(allimgs):
        if np.ndim(img) == 2:
            allimgs[i] = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        allimgs[i] = cv2.resize(img, dsize=(0, 0), fx=scale, fy=scale)
    w, h = allimgs[0].shape[1], allimgs[0].shape[0]
    
    sub = int(order[0] * order[1] - len(imglist))
   
    if sub > 0:
        for s in range(sub):
            allimgs.append(np.zeros_like(allimgs[0]))
    elif sub < 0:
        allimgs = allimgs[:sub]
    imgblank = np.zeros((h * order[0], w * order[1], 3), np.uint8)
    for i in range(order[0]):
        for j in range(order[1]):
            imgblank[i * h:(i + 1) * h, j * w:(j + 1) * w, :] = allimgs[i * order[1] + j]
    return imgblank


def main():
    parser = ArgumentParser()
    parser.add_argument('videoroot', help='imgroot for cameras, no more than 9 video', default=None, type=str)
    parser.add_argument('--csv', help='id of picture', default=None, type=str)

    args = parser.parse_args()

    frame_count_y = 0
    frame_count = 0
    pause = True
    right = False
    left = False
    fps = 30
    n = 1
    videos = []
    save_path_p = []
    cap_play = []

    for (rt, dr, files) in os.walk(args.videoroot):
        
        if files != []:
            for item in files:
                if item.endswith('avi') or item.endswith('m3u8'):
                    videos.append(os.path.join(rt, item))
    print(videos)
    
    if len(videos) < 10:
        print('功能介绍：')
        print('没有csv文件的话,保存图片时以帧数命名')
        print('空格:视频开始播放/暂停播放')
        print('a/d:控制图片翻页(可长按)')
        print('w/s:加快/减速视频播放速度')
        print('p:解压当前图片并保存到视频所在的文件夹')
        print('esc:退出视频播放')
        print('可以拖动视频下方的滑块来调节进度')
        print('视频播放完成后或者退出视频播放后,可选择是否对整个视频解压并保存到与视频名称位置都相同的文件夹')
        for a in videos:
            save_path_p.append(os.path.dirname(os.path.abspath(a)))
            cap_play.append(cv2.VideoCapture(a))
    else:
        print('一次最多只能观看9个视频')
        return
    
    frames = cap_play[0].get(cv2.CAP_PROP_FRAME_COUNT)
    frames_width = int(cap_play[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    frames_height = int(cap_play[0].get(cv2.CAP_PROP_FRAME_HEIGHT))

    for i in range(len(videos)):
        if int(cap_play[i].get(cv2.CAP_PROP_FRAME_WIDTH)) != frames_width or int(cap_play[0].get(cv2.CAP_PROP_FRAME_HEIGHT)) != frames_height:
            print('视频之间的w,h不同,无法一起查看')
            return

    cv2.namedWindow('show',0)
    cv2.resizeWindow('show', 1280 , 960)
    cv2.createTrackbar('frame', 'show', 0 ,int(frames)-1,nothing)


    while cap_play[0].isOpened():
        ret_play = []
        frame_play = []
        frame_resize = []
        for b in range(len(videos)):
            ret_play_x,frame_play_x = cap_play[b].read()
            ret_play.append(ret_play_x)
            frame_play.append(frame_play_x)
            # frame_resize.append(cv2.resize(frame_play_x, (480, 320)))

        if ret_play[0]:
            cv2.setTrackbarPos('frame', 'show', frame_count)
            if len(videos) == 1:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(1,1)))
            elif len(videos) == 2:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(1,2)))
            elif len(videos) == 3:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,2)))
            elif len(videos) == 4:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,2)))
            elif len(videos) == 5:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,3)))
            elif len(videos) == 6:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,3)))
            elif len(videos) == 7:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,4)))
            elif len(videos) == 8:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(2,4)))
            elif len(videos) == 9:
                cv2.imshow('show', cv2showimgs(scale= 1 , imglist= frame_play , order=(3,3)))
            
        else:
            print("视频播放完成")
            break
        
        key = cv2.waitKey(fps)
    
        if key == 27:
            break
        elif key == ord(' '):
            pause = not pause
        
        if args.csv is not None:
            with open(args.csv, encoding="utf-8-sig",mode="r") as f:
                reader = csv.reader(f)
                column = [row[1] for row in reader]
                id = column[frame_count]
        else:
            id = frame_count

        if key == ord('p'):
            if len(videos) == 1:

                print('解压当前第{}帧图片'.format(id))
                cv2.imwrite(os.path.join(save_path_p[0],str(id)+'.png'),frame_play[0])
            else:
                print('解压所有视频当前帧的图片还是单独解压某一个视频')
                while True:
                    p_choice = input('y表示解压所有的 数字表示解压某一个视频的编号一行一列编号为1 n退出 \n')
                    if p_choice == '1' or p_choice == '2' or p_choice == '3' or p_choice == '4' or p_choice == '5' or p_choice == '6' or p_choice == '7' or p_choice == '8' or p_choice == '9':
                        print('解压第{}个视频的{}图片到视频所在的文件夹'.format(int(p_choice),id))
                        cv2.imwrite(os.path.join(save_path_p[int(p_choice)-1],str(id)+'.png'),frame_play[int(p_choice)-1])
                    elif p_choice == 'n' or p_choice == 'N':
                        break
                    elif p_choice == 'y' or p_choice == 'Y':
                        print('解压所有视频的{}图片到每个视频所在的文件夹'.format(id))
                        for d in range(len(videos)):
                            cv2.imwrite(os.path.join(save_path_p[d],str(id)+'.png'),frame_play[d])
                    else:
                        print("无效指令,请重新输入")
                print("点击图像窗口，按空格继续播放视频")

        
        if key == ord('w'):
            fps = int(fps / 2)
            n = n * 2
            print('当前视频以{}倍速播放'.format(n))

        if key == ord('s'):
            fps = fps * 2
            n = n / 2
            print('当前视频以{}倍速播放'.format(n))
            
        frame_change = cv2.getTrackbarPos('frame', 'show')
        
        if frame_change != frame_count:

            for c in range(len(videos)):
                cap_play[c].set(1, frame_change)

            frame_count = frame_change
        

        if key == ord('a'):
            frame_count -= 1
            left = True
            # for c in range(len(videos)):
            #     cap_play[c].set(1, frame_count)

        if key == ord('d'):
            # for a in videos:
            right = True
            cap_play[0] = cv2.VideoCapture(videos[0])
            frame_count += 1 
            
    
            # for c in range(len(videos)):
            #     cap_play[c].set(cv2.CAP_PROP_POS_FRAMES, frame_count)  
        
        if not pause:
            frame_count += 1
        else:
            # if right or left:
            #     pass
            # else:
         
            for c in range(len(videos)):
                cap_play[c].set(cv2.CAP_PROP_POS_FRAMES, frame_count)
    

    for m in range(len(videos)):
        cap_play[m].release()
    cv2.destroyAllWindows()

    print('是否对整个视频进行解压')
    save_path = []
    files_name_list = []
    
    cap_y = []
    frame_count_n = 0
    for x in videos:
        
        save_path.append(os.path.dirname(os.path.abspath(x)))
        
        file_name = os.path.basename(os.path.abspath(x))
        file_name = file_name.split('.')[0]
        files_name_list.append(file_name)

    while True:
        choice = input('y表示解压所有的 数字表示解压某一个视频的编号一行一列编号为1 n退出 \n')
        if choice == '1' or choice == '2' or choice == '3' or choice == '4' or choice == '5' or choice == '6' or choice == '7' or choice == '8' or choice == '9':
            print('创建与视频名称相同的文件夹来保存解压后的图片')
            cap = cv2.VideoCapture(videos[int(choice)-1])
            print('开始对第{}个视频进行解压'.format(int(choice)-1))
            os.mkdir(os.path.join(save_path[int(choice)-1],files_name_list[int(choice)-1]))
            while cap.isOpened():
                if args.csv is not None:
                    with open(args.csv, encoding="utf-8-sig",mode="r") as f:
                        reader = csv.reader(f)
                        column = [row[1] for row in reader]
                        id = column[frame_count_n]
                else:
                    id = frame_count_n
                
                ret_n, frame_n = cap.read()
                if not ret_n:
                        break
                cv2.imwrite(os.path.join(save_path[int(choice)-1],files_name_list[int(choice)-1],str(id)+'.png'),frame_n)
                print('已完成第{}个视频的{}的解压'.format(int(choice) , id))
                frame_count_n += 1
            cap.release()
            print('第{}}个视频解压完成'.format(int(choice)))
        elif choice == 'y' or choice == 'Y':
            print('创建与视频名称相同的文件夹来保存解压后的图片')
            for h in range(len(videos)):
                cap_y.append(cv2.VideoCapture(videos[h]))
                os.mkdir(os.path.join(save_path[h],files_name_list[h]))

            print('开始对所有视频进行解压')
            
            while cap_y[0].isOpened():
                if args.csv is not None:
                    with open(args.csv, encoding="utf-8-sig",mode="r") as f:
                        reader = csv.reader(f)
                        column = [row[1] for row in reader]
                        id = column[frame_count_y]
                else:
                    id = frame_count_y
                ret_y = []
                frame_y = []
                
                for o in range(len(videos)):
                    ret_x , frame_x = cap_y[o].read()
                    ret_y.append(ret_x)
                    frame_y.append(frame_x)
                if not ret_y[0]:
                    break
                
                for t in range(len(videos)):
                    cv2.imwrite(os.path.join(save_path[t],files_name_list[t],str(id)+'.png'),frame_y[t])
                print('已完成所有视频的{}的解压'.format(id))
                frame_count_y += 1
            for u in range(len(videos)):
                cap_y[u].release()
            print('所有视频解压完成')

            return
        elif choice == 'n' or choice =='N':
            return
        else:
            print('无效按键')



        





if __name__ == '__main__':
    main()

