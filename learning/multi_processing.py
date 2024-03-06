from multiprocessing import Process
import os

max_processes = 2

def time_sleep(sleep_time):
    pid = os.getpid()
    print(f'{pid} : {sleep_time}')
    os.system(f'sleep {sleep_time}')
    print(f'{pid}: sleep {sleep_time} end')

processes = []
    
processes.append(Process(target=time_sleep, args=(30,), name='process1'))
processes.append(Process(target=time_sleep, args=(20,), name='process2'))
processes.append(Process(target=time_sleep, args=(60,), name='process3'))
processes.append(Process(target=time_sleep, args=(10,), name='process4'))
processes.append(Process(target=time_sleep, args=(20,), name='process5'))

print(processes)
running = 0 
for process in processes:
    if running >= max_processes:
        process.start()
        running+=1
        process.join()
        running-=1
    else:
        process.start()
        running+=1
        
