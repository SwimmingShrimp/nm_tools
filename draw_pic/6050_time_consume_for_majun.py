import numpy as np
import time
import matplotlib.pyplot as plt

txt = '/home/lixialin/Downloads/log/nmlog_defualt.1.log'
all_time_list = []
time_list = ['11111','22222','33333','44444','55555','66666','77777','88888']
with open(txt,'r') as f:
    for line in f.readlines():
        for temp in time_list:
            if temp in line:
                h,m,M = line.split(' ')[2].split(':')
                t = (int(h)*3600 + int(m)*60 + float(M))*1000
                all_time_list.append(t)
time_diff_list = []
for i in range(len(all_time_list)-1):
    time_diff = all_time_list[i+1] -all_time_list[i]
    time_diff_list.append(time_diff)
t12 = time_diff_list[::8][::20]
t23 = time_diff_list[1::8][::20]
t34 = time_diff_list[2::8][::20]
t45 = time_diff_list[3::8][::20]
t56 = time_diff_list[4::8][::20]
t67 = time_diff_list[5::8][::20]
t78 = time_diff_list[6::8][::20]
t81 = time_diff_list[7::8][::20]

plt.figure(figsize=(180,80),dpi=100)
x = [m for m in range(len(t12))]
plt.title('Time Consuming', fontproperties='SimHei')
plt.plot(x,t23)
plt.plot(x,t45)
plt.plot(x,t56)
plt.plot(x,t67)
plt.xlabel('counts')
plt.ylabel('time_consuming(ms)')
plt.legend(['Side_Obstacle','Lane','Freespace','Front_Obstacle'])
plt.show()
# print(len(t12),len(t81))
# print('t12_avg =' ,sum(t12)/len(t12))
# print('t23_avg =' ,sum(t23)/len(t23))
# print('t34_avg =' ,sum(t34)/len(t34))
# print('t45_avg =' ,sum(t45)/len(t45))
# print('t56_avg =' ,sum(t56)/len(t56))
# print('t67_avg =' ,sum(t67)/len(t67))
# print('t78_avg =' ,sum(t67)/len(t67))
# print('t81_avg =' ,sum(t81)/len(t81))


