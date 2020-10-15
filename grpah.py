from matplotlib import pyplot as plt
import csv
import numpy as np
from matplotlib import pyplot as plt
import os

def readfile(path,filename):
    filename=path+filename
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
def draw_pyplot(title,y_label,y_value,file_path):
    #x_value=list()
    colors=["r","g","b","c","m"]
    for i in range(len(y_value)):
        x_value = np.arange(len(y_value[i]))
        plt.xlabel("Time")
        plt.ylabel(y_label)
        plt.title(title)
        plt.plot(x_value,y_value[i],color=colors[i])
        #plt.fill_between(x_value,ymin,y_value[i])
        plt.legend(labels=("AdaMM","One server"))
    plt.show(block=False)
    plt.savefig(file_path + title + ".png")
    plt.clf()



def draw_subplot(title,y_label,y_value):
    for i in range(len(y_value)):
        x_value = np.arange(len(y_value[i]))
        flg, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel("Time")
        ax.set_ylabel(y_label)
        ax.plot(x_value, y_value[i])
    2020
    _ETRI_가천대학교_0921
    #plt.show()

def get_files(path):
    file_list=os.listdir(path)
    file_list.remove("One_server_GPU_usage.csv")
    return file_list

#Video1 : 총 60초 / 사람 없는 시간 약 6초~55초 (49초)
#Video2 : 총 40초 / 사람 없는 시간 약 6초 ~33(27초)
#Video3 : 총 54초 / 사람 없는 시간 2초~26초 약 34초~49초

if __name__ == '__main__':
    """
    for j in range(3):
        each_video_path="data/video"+str(j+1)+"/"
        each_graph_path="data/graph/video"+str(j+1)+"/"
        file_list=get_files(each_video_path)
        for i in range(len(file_list)):
            gpu_usage_adamm,gpu_memory_adamm=readfile(each_video_path,file_list[i])
            gpu_usage_one,gpu_memory_one=readfile(each_video_path,"One_server_GPU_usage.csv")

            compare_memory=combine_list(gpu_memory_adamm,gpu_memory_one)
            compare_usage=combine_list(gpu_usage_adamm,gpu_usage_one)

            draw_pyplot("GPU Memory usage (Adamm vs One-server)"+file_list[i][16:26],"GPU memory usage(%)",compare_memory,each_graph_path)

            draw_pyplot("GPU Utils (Adamm vs One-server)"+file_list[i][16:26],"GPU utils usage(%)",compare_usage,each_graph_path)
    """
    qdrop=[897,896,894]
    endtime=[61,61,61]
    x_labe=["10","20","30"]

    flg, ax = plt.subplots()
    ax.set_title("Frame drop (size of queue :40)")
    ax.set_xlabel("Timeout")
    ax.set_ylabel("number of frame drop")
    ax.plot(x_labe,qdrop)
    plt.show(block=False)
    plt.savefig("data/graph/graph3.png")
    plt.clf()






