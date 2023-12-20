import os
import matplotlib.pyplot as plt
import re
import numpy as np

# front
def draw_front_fps():
    txt = '/home/lixialin/Music/system/front/fps.log'
    frame_rate_list = []
    delay_time = []
    with open(txt,'r') as f:
        for line in f.readlines():
            line = re.sub('\n','',line)
            if 'delay' in line:
                delay_time.append(int(line.split('delay: ')[-1].split(' ms')[0]))
            if 'fps:' in line:
                frame_rate = round(float((line.split('fps: ')[-1].split(' ')[0]).strip()),1)
                frame_rate_list.append(frame_rate)
    delay_len = int(len(delay_time))
    delay_time = delay_time[1:delay_len]
    fps_len = int(len(frame_rate_list))
    frame_rate_list = frame_rate_list[1:fps_len]
    # frame_rate_list = frame_rate_list[::10]
    # delay_time = delay_time[::10]
    print(delay_time)

    plt.figure(figsize=(180,80),dpi = 100)
    x  = [m for m in range(fps_len-1)]
    plt.ylim(0,200)
    plt.title('FPS & DelayTime : front&side&back camera')
    plt.plot(x, frame_rate_list)
    plt.plot(x, delay_time)
    # plt.grid(True)
    plt.legend(['FPS','DelayTime'],loc='lower right')
    plt.xlabel('FrameID')
    plt.ylabel('FPS & DelayTime')
    plt.show()

def draw_fisheye_fps():
    txt = '/home/lixialin/Music/system/fisheye/fps.log'
    frame_rate_list = []
    delay_time = []
    with open(txt,'r') as f:
        for line in f.readlines():
            line = re.sub('\n','',line)
            if 'delay' in line:
                delay_time.append(int(line.split('delay: ')[-1].split(' ms')[0]))
            if 'fps:' in line:
                frame_rate = round(float((line.split('fps: ')[-1].split(' ')[0]).strip()),1)
                frame_rate_list.append(frame_rate)
    delay_len = int(len(delay_time))
    delay_time = delay_time[1:delay_len]
    fps_len = int(len(frame_rate_list))
    frame_rate_list = frame_rate_list[1:fps_len]
    plt.figure(figsize=(180,80),dpi = 100)
    x  = [m for m in range(fps_len-1)]
    plt.ylim(0,100)
    plt.title('FPS & DelayTime : fisheye camera')
    plt.plot(x, frame_rate_list)
    plt.plot(x, delay_time)
    plt.legend(['FPS','DelayTime'],loc='lower right')
    plt.xlabel('FrameID')
    plt.ylabel('FPS & DelayTime')
    plt.show()

def main():
    # draw_front_fps()
    draw_fisheye_fps()

if __name__=='__main__':
    main()