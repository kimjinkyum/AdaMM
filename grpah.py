from matplotlib import pyplot as plt
import csv
import numpy as np
from matplotlib import pyplot as plt

def readfile(filename):
    filename="data/"+filename
    with open(filename, 'r') as f:
        reader = csv.reader(f)

        result=list()
        for row in reader:
            result.append(row)
    print("[System] End of reading file")
    tmp1=result[0]
    tmp2=result[2]

    return conver_str_to_float(tmp1[1:]),conver_str_to_float(tmp2[1:])

def combine_list(adamm,one):
    result = list()
    #adamm=adamm[0:len(adamm)]
    result.append(adamm)
    result.append(one)
    return result

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
        x_value = np.arange(len(y_value[i]))/2
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)



        ymin=min(y_label[i])
        ymax=max(y_label[i])
        plt.plot(x_value,y_value[i],color=colors[i])
        #plt.fill_between(x_value,ymin,y_value[i])
        plt.legend(labels=("AdaMM","One server"),loc="upper right")
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

#약 22초 비디오 실행 했을 때
gpu_usage_adamm,gpu_memory_adamm=readfile("AdaMM_GPU_usage.csv")
gpu_usage_one,gpu_memory_one=readfile("One_server_GPU_usage.csv")

print(gpu_usage_adamm)
print(gpu_usage_one)

compare_memory=combine_list(gpu_memory_adamm,gpu_memory_one)
compare_usage=combine_list(gpu_usage_adamm,gpu_usage_one)

draw_pyplot("GPU Memory usage (Adamm vs One-server)","GPU memory usage(%)",compare_memory)
draw_pyplot("GPU Utils (Adamm vs One-server)","GPU utils usage(%)",compare_usage)