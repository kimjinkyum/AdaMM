import socket
import time
import numpy as np
import cv2

video_path="C:\\Users\\kimos\\Desktop\\pose estimation\\tf-pose-estimation\\example_video1.mp4"
cam = cv2.VideoCapture(video_path)
fps=cam.get(cv2.CAP_PROP_FPS)
totalFrames=cam.get(cv2.CAP_PROP_FRAME_COUNT)
print(float(totalFrames)/fps)
print(totalFrames)
print(fps)

i=0
sleep_time=0
start_time=time.time()
while True:

    ret, img = cam.read()
    if img is None:
        break



    if i>68 and i<600:
        if i==69:
            sleep_time=time.time()
            print("Frist start_time",sleep_time-start_time)
        if i==599:
            print("Frist",time.time()-sleep_time)
        cv2.imshow('None', img)
        _ = 0xFF & cv2.waitKey(1)

    elif i>835 and i<1405:
        if i==846:
            sleep_time=time.time()
            print("second start_time", sleep_time-start_time)
        if i==1404:
            print("Second",time.time()-sleep_time)
        cv2.imshow('None', img)
        _ = 0xFF & cv2.waitKey(1)
    else:
        #pass
        cv2.imshow('None', img)
        _ = 0xFF & cv2.waitKey(1)
    i+=1
print(time.time()-start_time)
print(i)
