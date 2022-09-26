import os
import matplotlib.pyplot as plt
import re
import numpy as np
from matplotlib.pyplot import MultipleLocator

txt = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/nullmax/7.2_version_test_results/mona_v4.0_1/lxl.log'
sensor0_frame_rate_list,sensor1_frame_rate_list,sensor4_frame_rate_list,sensor5_frame_rate_list,sensor6_frame_rate_list,sensor7_frame_rate_list = [],[],[],[],[],[]
with open(txt,'r') as f:
    for line in f.readlines():
        line = re.sub('\n','',line) 
        frame_rate = (line.split(':')[-1]).strip()
        if frame_rate!='':
            frame_rate = round(float(frame_rate),2)
            if 'Sensor0' in line:
                sensor0_frame_rate_list.append(frame_rate)
            elif 'Sensor1' in line:
                sensor1_frame_rate_list.append(frame_rate)
            elif 'Sensor4' in line:
                sensor4_frame_rate_list.append(frame_rate)
            elif 'Sensor5' in line:
                sensor5_frame_rate_list.append(frame_rate)
            elif 'Sensor6' in line:
                sensor6_frame_rate_list.append(frame_rate)
            elif 'Sensor7' in line:
                sensor7_frame_rate_list.append(frame_rate)
plt.figure(figsize=(180,80),dpi = 100)

x  = [m for m in range(len(sensor0_frame_rate_list))]
_yticks_labels = np.arange(12,16,0.5)
plt.yticks(_yticks_labels)
plt.subplot(1, 2, 1)
plt.title('front stereo camera online realtime frame rate')
plt.plot(x, sensor0_frame_rate_list,label='front_far')
plt.plot(x, sensor1_frame_rate_list,label='front_near')
plt.xlabel('frame_id')
plt.ylabel('frame_rate')
plt.legend()
plt.subplot(1, 2, 2)
plt.title('side camera online realtime frame rate')
plt.plot(x, sensor4_frame_rate_list,label='side_left_front')
plt.plot(x, sensor5_frame_rate_list,label='side_left_rear')
plt.plot(x, sensor6_frame_rate_list,label='side_right_front')
plt.plot(x, sensor7_frame_rate_list,label='side_right_rear')
plt.legend()
# for a, b in zip(x, sensor4_frame_rate_list):
#     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
plt.xlabel('frame_id')
plt.ylabel('frame_rate')
plt.show()