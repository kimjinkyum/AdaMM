import time
import sys
import cv2
import time
import pickle
import argparse
import zlib
import logging
import subprocess as sp
import os,multiprocessing
import socket
import threading
import struct
import numpy as np

import config

import ipywidgets as widgets
from subprocess import check_output
import re

ls=[]
def nvidia_smi(options=['-q','-d','MEMORY']):
    return check_output(['nvidia-smi'] + options)
def update_widget(w=None, new_box=False):
    if w is None:
        w = widgets.Textarea(
            value=nvidia_smi(),
            placeholder='nvidia-smi output',
            width=100,
            disabled=False
        )
        #display(w)
        return w
    else:
        w.value = nvidia_smi()
        if new_box:
            return w
        else:
            return None

def nvidia_stats():
    out = update_widget()
    out=out.value
    k=out.split("\n")
    used=re.findall("\d+", k[11])[0]
    #print(k[11])#used Memory
    #print(out)
    #print(type(out.value))
    #used=0
    #total = int(out[9].split()[2])
    #units = out[10].split()[3]
    #used = out[10].split()[2]
    ls.append(used)
    print("GPU",used)
    
#init 부분 
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
def init():
    
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    
    parser.add_argument('--tensorrt', type=str, default="False",
                        help='for tensorrt process.')
    args = parser.parse_args()
    return args

def model_init():
    from tf_pose.estimator import TfPoseEstimator
    from tf_pose.networks import get_graph_path, model_wh
    args=init()
    s=time.time()
    print("start tensorflow")
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), trt_bool=str2bool(args.tensorrt))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), trt_bool=str2bool(args.tensorrt))
    print("Timing init",time.time()-s)
    return args, e,w,h

# flag : 0 ---> model init, image Nond 1--> model init후 image  받을 때 2--> terminate 후
def tracking(image,flag,d):
    from tf_pose.estimator import TfPoseEstimator

    if flag==0:
        args,e,w,h=model_init()
    else if flag==1:
        motion_tracking(args,e,w,h,image)
    else:
        args,e,w,h=model_init()
        motion_tracking(args,e,w,h,image)
       
def motion_tracking(args,e,w,h,decimg):
    fps_time = time.time()
    print("in function")
    humans = e.inference(decimg, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
    y1=[0.0]
    y=0
    image = TfPoseEstimator.draw_humans(decimg, humans, imgcopy=False)
    for human in humans:
        for i in range(len(humans)):
            try :
                a=human.body_parts[0]
                x=a.x*image.shape[1]
                y=a.y*image.shape[0]
                y1.append(y)
                    #print(y1[-2])
            except:
                pass
            if ((y-y1[len(y1)-2])>30):
                print("fall",i+1)
                #send_data={"name" :"fall"}
                #r=requests.post("http://127.0.0.1:5000/http",json=send_data)

    cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
    cv2.imshow('tf-pose-estimation result', image)
def motion(data):
    if data==0:
        model_init()
    return data+2

if __name__=="__main__":
    
    pool = multiprocessing.Pool()
    manager=multiprocessing.Manger()
    d=manager.dict()
    d['e']=config.variable1
    i=0
    flag=0
    cam = cv2.VideoCapture("C:\\Users\\user01\\Desktop\\tf-pose-estimation\\t1.mp4")
    while True:
        ret_val, frame = cam.read()     
        if i>10:
            break
        if (i % 2) == 0: # use mod operator to see if "i" is even
            print(i,"th",flag)
            if flag==0:
                print(pool.apply_async(motion,(frame,flag,d)))
                nvidia_stats()
                flag=1
            else:
                print(pool.apply(motion,(i,)))
                nvidia_stats()
                       
        else:
            if i==3: 
                pool.terminate()
                flag=0
                print("terminate")
                nvidia_stats()
                pool.join()
                pool=multiprocessing.Pool()
        i=i+1