import os
from unicodedata import decimal
import matplotlib.pyplot as plt
from matplotlib import ticker
import re
import numpy as np

txt = '/home/lixialin/Downloads/0305感知负载延迟真率log/front_side_back/mem.log'
mem = []
with open(txt,'r') as f:
    for line in f.readlines():
        if './bin/sensor_' in line:
            mem.append(int(line.strip().split(' ')[-1][:-1])/100)
# mem = mem[::2]
x  = [m for m in range(len(mem))]
plt.ylim(0.0,0.06)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=1))
# plt.title('Memory Usage:front&side&back camera')
plt.title('Memory Usage:fisheye camera')
plt.plot(x, mem,label='memory usage')
plt.legend(loc='lower right')
plt.xlabel('number of samples')
plt.ylabel('memory usage')
plt.show()
