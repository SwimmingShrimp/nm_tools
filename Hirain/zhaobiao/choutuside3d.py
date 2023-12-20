import random, shutil
import argparse
import os
from PIL import Image

parser = argparse.ArgumentParser()

parser.add_argument('imgroot', help='img root',default=None, type=str)
args = parser.parse_args()

img = []
root = []

def copyFile(fileDir,tardir):
        pathDir = os.listdir(fileDir)    #取图片的原始路径
        filenumber=len(pathDir)
        rate=0.05    #自定义抽取图片的比例，比方说100张抽10张，那就是0.1
        picknumber=int(filenumber*rate) #按照rate比例从文件夹中取一定数量图片
        sample = random.sample(pathDir, picknumber)  #随机选取picknumber数量的样本图片
        print (sample)
        for name in sample:
                shutil.copy(os.path.join(fileDir,name), os.path.join(tardir,name))
                shutil.copy(os.path.join(fileDir.replace("SideFrontLeft","SideFrontRight"),name), os.path.join(tardir.replace("SideFrontLeft","SideFrontRight"),name))
                shutil.copy(os.path.join(fileDir.replace("SideFrontLeft","SideRearLeft"),name), os.path.join(tardir.replace("SideFrontLeft","SideRearLeft"),name))
                shutil.copy(os.path.join(fileDir.replace("SideFrontLeft","SideRearRight"),name), os.path.join(tardir.replace("SideFrontLeft","SideRearRight"),name))
        return

for (rt, dr, files) in os.walk(args.imgroot):

        if files != []:
            root.append(rt)

for rt in root:
    filedir = rt
    tardir = rt.replace("HengRun_WaterMark","HengRun_WaterMark_20")
    if os.path.exists(tardir):
        pass
    else:
        os.makedirs(tardir)
    
    if os.path.exists(tardir.replace("SideFrontLeft","SideFrontRight")):
        pass
    else:
        os.makedirs(tardir.replace("SideFrontLeft","SideFrontRight"))
    
    if os.path.exists(tardir.replace("SideFrontLeft","SideRearLeft")):
        pass
    else:
        os.makedirs(tardir.replace("SideFrontLeft","SideRearLeft"))
    
    if os.path.exists(tardir.replace("SideFrontLeft","SideRearRight")):
        pass
    else:
        os.makedirs(tardir.replace("SideFrontLeft","SideRearRight"))
    copyFile(filedir,tardir)