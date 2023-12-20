import os
import matplotlib.pyplot as plt
from matplotlib  import ticker
import re
import numpy as np

txt = '/media/lixialin/b4228689-0850-4159-ad34-8eaba32c783d/04_test_results/v7.1.1/systemtest_result_front_15h/v7.1.1_cpu_15h.log'
CPU0,CPU1 = [],[]
with open(txt,'r') as f:
    for line in f.readlines():
        if 'CPU 0 idle: ' in line:
            CPU0.append((100-int(line.split(' ')[-2].split('%')[0]))/100)
        elif 'CPU 1 idle: ' in line:
            CPU1.append((100-int(line.split(' ')[-2].split('%')[0]))/100)

x  = [m for m in range(len(CPU0))]
CPU_avg =[]
for i in range(len(x)):
    CPU_avg.append((CPU0[i] + CPU1[i])/2)
plt.ylim(0.0,1.0)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=1))
plt.title('Bunding CPU:front&side&back camera')
# plt.title('Bunding CPU:fisheye camera')
plt.plot(x, CPU0,label='CPU0')
plt.plot(x, CPU1,label='CPU1')
plt.plot(x, CPU_avg,label='CPU_AVG')
plt.legend(loc='lower right')
plt.xlabel('number of samples')
plt.ylabel('cpu usage')
plt.show()