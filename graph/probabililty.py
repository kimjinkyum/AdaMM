#!/usr/bin/env python
# coding: utf-8

# In[5]:


import argparse
import random
import numpy as np
import time
import cv2


# In[6]:


video_path = "C://Users//jinkyum//Desktop//pose//video//prob.mp4"
cam = cv2.VideoCapture(video_path)

frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cam.get(cv2.CAP_PROP_FPS)
total_time = int(frame_count / fps)

print(frame_count)
print(total_time)


# In[8]:


#Prob : 오브젝트가 총 % 출현
#X : object 가 출현 했을 때 몇 frame (몇 초 나오는지)
def select_random(prob, X,fps,frame_count):
    #fps, total_time = cam_read()
    #print(total_time)
    total_time = int(frame_count / fps)
    object_time = int(total_time * prob)
    occupy_frame = int(fps *X)
    print(occupy_frame)
    
    
    random_list = np.arange(0,int(frame_count),3).tolist()
    
    random_index = sorted(random.sample(random_list, int(object_time *fps / occupy_frame)))
    print(object_time)
    
    print(len(random_index))
    return random_index, occupy_frame


# In[9]:


random_index, occupy_frame=select_random(0.1, 1,fps,frame_count)


# In[13]:


def send(selected_index, occupy_frame, path):
    cam = cv2.VideoCapture(video_path)
    i = 0
    frame_index = 0
    while True:
        ret, img = cam.read()
        if img is None:
            break
        i+=1
        if frame_index <len(selected_index):
            if i == selected_index[frame_index]:
                for j in range(occupy_frame):
                    #print("Select frame",selected_index[frame_index]+j)
                    cv2.imshow('tf-pose-estimation result', img)
                    _ = 0xFF & cv2.waitKey(1)
                frame_index+=1
                      
    print(i)


# In[14]:


send(random_index, occupy_frame, video_path)

