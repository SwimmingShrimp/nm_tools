# 将avi转成png
import cv2
import os

src = '/home/lixialin/Pictures/SideFrontLeft.mp4'
save_dir = '/home/lixialin/Pictures/pic/'

cap = cv2.VideoCapture(src)
frame_count = 0  # 给每一帧标号
while True:
    frame_count += 1
    flag, frame = cap.read()
    if not flag:  # 如果已经读取到最后一帧则退出
        break
    if os.path.exists(
            save_dir + str(frame_count) + '.png'):  # 在源视频不变的情况下，如果已经创建，则跳过
        break
    picname = str(frame_count) + '.png'
    cv2.imwrite(os.path.join(save_dir,picname),frame)
cap.release()
