#!/usr/bin/python
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib import ticker
import re

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('logpath',type=str, help='日志文件路径')
    parser.add_argument('type',type=str, help='画的类别，cpu、fps、mem')
    parser.add_argument('camera',type=str, help='相机，front_side_back/fisheye')
    parser.add_argument('savefig',type=str, help='保存画好的cpu,fps等图片的位置')
    args = parser.parse_args()
    return args

def cpu(logpath,camera,title,savefig):
    cpu_list =  []
    txt=os.path.join(logpath,'fps_'+ camera +'.log')
    with open(txt,'r') as f:
        for line in f.readlines():
            line = re.sub('\n','',line)
            if ' cpu: ' in line:
                cpu_list.append(float(line.split('cpu: ')[-1])/200)
    cpu_list = cpu_list[2:]
    x  = [m for m in range(len(cpu_list))]
    plt.figure(figsize=(18,10))
    plt.ylim(0.0,1.0)
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=1))
    plt.title(title)
    plt.plot(x, cpu_list,label='cpu')
    plt.legend(loc='lower right')
    plt.xlabel('number of samples')
    plt.ylabel('cpu usage')
    plt.grid(True)
    plt.savefig(os.path.join(savefig,'cpu_'+camera+'.png'))
    
def mem(logpath,camera,title,savefig):
    txt=os.path.join(logpath,'mem_'+ camera +'.log')
    mem = []
    with open(txt,'r') as f:
        for line in f.readlines():
            if './bin/sensor_' in line:
                mem.append(int(line.strip().split(' ')[-1][:-1])/100)
    x  = [m for m in range(len(mem))]
    plt.figure(figsize=(18,10))
    plt.ylim(0.0,0.2)
    plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=1))
    plt.plot(x, mem,label='memory usage')
    plt.legend(loc='lower right')
    plt.xlabel('number of samples')
    plt.title(title)
    plt.grid(True)
    # plt.show()
    plt.savefig(os.path.join(savefig,'mem_'+camera+'.png'))

def fps(logpath,camera,title,savefig,ylim):
    txt=os.path.join(logpath,'fps_'+ camera +'.log')
    frame_rate_list = []
    delay_time = []
    with open(txt,'r') as f:
        for line in f.readlines():
            line = re.sub('\n','',line)
            if ' delay: ' in line:
                delay_time.append(int(line.split('delay: ')[-1].split(' ms')[0]))
            if ' fps: ' in line:
                frame_rate_list.append(round(float((line.split('fps: ')[-1].split(' ')[0])),1))
    delay_time = delay_time[2:]
    frame_rate_list = frame_rate_list[2:]
    lens = len(delay_time)
    plt.figure(figsize=(18,10))
    x  = [m for m in range(lens)]
    plt.ylim(ylim)
    plt.title(title)
    plt.plot(x, frame_rate_list)
    plt.plot(x, delay_time)
    plt.grid(True)
    plt.legend(['FPS','DelayTime'],loc='lower right')
    plt.xlabel('FrameID')
    plt.ylabel('FPS & DelayTime')
    # plt.show()
    plt.savefig(os.path.join(savefig,'fps_'+camera+'.png'))



if __name__ == '__main__':
    args = parse_args()
    logpath = args.logpath
    type = args.type
    camera = args.camera
    savefig = args.savefig

    if type=='cpu' and camera=='front_side_back':
        title = "Bunding CPU:front&side&back camera"
        cpu(logpath,camera,title,savefig)
    if type=='cpu' and camera=='fisheye':
        title = "Bunding CPU:fisheye camera"
        cpu(logpath,camera,title,savefig)
    if type=='mem' and camera=='front_side_back':
        title = "Memory Usage:front&side&back camera"
        mem(logpath,camera,title,savefig)
    if type=='mem' and camera=='fisheye':
        title = "Memory Usage:fisheye camera"
        mem(logpath,camera,title,savefig)
    if type=='fps' and camera=='front_side_back':
        title = "FPS & DelayTime:front&side&back camera"
        ylim = (0,250)
        fps(logpath,camera,title,savefig,ylim)
    if type=='fps' and camera=='fisheye':
        title = "FPS & DelayTime:fisheye camera"
        ylim = (0,100)
        fps(logpath,camera,title,savefig,ylim)
