import os
import matplotlib.pyplot as plt
import re
import numpy as np

txt = '/home/lixialin/Music/v6.1.3/systemtest_result_4h/fps.log'
delay_time = []
with open(txt,'r') as f:
    for line in f.readlines():
        if 'delay' in line:
            delay_time.append(int(line.split('delay')[-1].split('ms')[0][1:]))
# delay_time = delay_time[::10]
lens = int(len(delay_time))
x  = [m for m in range(lens)]
delay_time = delay_time[0:lens]
plt.ylim(0,250)
# plt.title('Delay Time:front&side&back camera')
plt.title('Delay Time:fisheye camera')
plt.plot(x, delay_time,label='delay time')
plt.legend(loc='lower right')
plt.xlabel('frame id')
plt.ylabel('delay_time(ms)')
plt.show()