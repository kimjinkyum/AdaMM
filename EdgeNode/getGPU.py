# Get GPU usage value on 1 sec

from usage import nvidia_stats,write
import cv2
import keyboard
import threading

"""
if len(ls)>3:
        t.cancel()
        print("End")
        #write(t)
"""

def run():
    t=threading.Timer(1, run)
    t.start()
    nvidia_stats()
    if keyboard.is_pressed('q') :
        print(write())
        t.cancel()
    
run()