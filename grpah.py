from matplotlib import pyplot as plt
import csv
import numpy as np
from matplotlib import pyplot as plt

def readfile(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        result=list()
        for row in reader:
            result.append(row)
    print("[System] End of reading file")
    return result[0],result[2]

def conver_str_to_float(value):
    for i in range(len(value)):
        value[i]=float(value[i])
    return value

#x_value: time
#보통 y_value[0]=AdaMM  y_value[1]=One-server
def draw_pyplot(title,y_label,y_value):
    #x_value=list()
    colors=["r","g","b","c","m"]
    for i in range(len(y_value)):
        x_value = np.arange(len(y_value[i]))
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.plot(x_value,y_value[i],color=colors[i])
        plt.legend(labels=("AdaMM","One-server"),loc="upper right")
    plt.show()

def draw_subplot(title,y_label,y_value):
    for i in range(len(y_value)):
        x_value = np.arange(len(y_value[i]))
        flg, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(y_label)
        ax.plot(x_value, y_value[i])
    plt.show()

gpu_usage,gpu_memory=readfile("GPU_usage.csv")
gpu_usage=conver_str_to_float(gpu_usage[1:])
gpu_memory=conver_str_to_float(gpu_memory[1:])

temp=list()
for i in range(len(gpu_usage)):
    temp.append(gpu_usage[i]+i)

result=list()
result.append(gpu_usage)
result.append(temp)


draw_pyplot("GPU usage (Adamm vs One-server)","GPU usage(%)",result)
