from collections import defaultdict
import argparse


import sys
#import keyboard
import threading
from threading import Thread

from subprocess import check_output
import csv
import time
import os
import numpy as np
from subprocess import Popen,PIPE

class GPUusge(Thread):

    def __init__(self,args):
        super().__init__()
        self.usage_list = defaultdict(list)
        self.stop_flag = threading.Event()
        self.file_name = "Prob:" + str(args.prob) + "occupy time" + str(args.X) + "Timeout" + str(args.timeout)

    def stop(self):
        self.stop_flag.set()

    def stopped(self):
        return self.stop_flag.isSet()

    def run(self):
        while True:
            if self.stopped():
                self.write_file(self.file_name)
                return
            self.getGPU()
            time.sleep(0.9)

    def getlist(self):
        return self.usage_list

    def safeFloatCast(self,strNumber):
        try:
            number = float(strNumber)
        except ValueError:
            number = float('nan')
        return number

    def getGPU(self):
        p = Popen(['nvidia-smi',
                   "--query-gpu=index,uuid,utilization.gpu,memory.total,memory.used,memory.free,driver_version,name,gpu_serial,display_active,display_mode,temperature.gpu",
                   "--format=csv,noheader,nounits"], stdout=PIPE)
        stdout, stderror = p.communicate()
        output = stdout.decode('UTF-8')
        lines = output.split(os.linesep)
        vals=lines[0].split(",")
        self.match_list(vals)

    def write_file(self):
        result=self.getlist()
        filename=self.file_name+".csv"
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            for k, v in result.items():
                writer.writerow([k] + v)
        print("[System] End of writing file")
        sys.exit(0)


    def match_list(self,vals):
        for i in range(12):
            #print(vals[i])
            if (i == 0):
                deviceIds = (vals[i])
            elif (i == 1):
                uuid = vals[i]
            elif (i == 2):
                gpuUtil = self.safeFloatCast(vals[i]) / 100
            elif (i == 3):
                memTotal = self.safeFloatCast(vals[i])
            elif (i == 4):
                memUsed = self.safeFloatCast(vals[i])
            elif (i == 5):
                memFree = self.safeFloatCast(vals[i])
            elif (i == 6):
                driver = vals[i]
            elif (i == 7):
                gpu_name = vals[i]
            elif (i == 8):
                serial = vals[i]
            elif (i == 9):
                display_active = vals[i]
            elif (i == 10):
                display_mode = vals[i]
            elif (i == 11):
                temp_gpu = self.safeFloatCast(vals[i])

        self.usage_list["GPU"].append(gpuUtil*100)
        self.usage_list["Memory"].append(float(memUsed)/float(memTotal)*100)

        #print("GPU",gpuUtil*100)
        #print("Memory",float(memUsed)/float(memTotal)*100)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send based object probability")
    parser.add_argument("--prob", type=float, default=1)
    parser.add_argument("--X", type=float, default=0.1)
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--time", type=float,default=330)
    args = parser.parse_args()

    gpu = GPUusge(args)
    #image = np.zeros((100,100,3),np.uint8)
    #cv2.imshow("keytest",image)
    #gpu.start()
    print("[GPU] start")
    s_time = time.time()
    k_time = time.time()
    j=0
    while True:    
        if time.time()-s_time > args.time : 
            #gpu.stop()
            gpu.write_file()
            print("[GPU] End")
            break
        elif time.time() - k_time >=1:
            k_time = time.time()
            gpu.getGPU()
            print(j)
            j=j+1
            
	    

    sys.exit(0)            
      



