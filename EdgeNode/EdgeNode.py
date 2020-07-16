import io
import socket
import struct
import time
import pickle
import argparse
import zlib
import numpy as np
import cv2
import logging
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


HOST='127.0.0.1' #Edge Your IP address
PORT=8000 
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


fps_time = 0
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
w, h = model_wh(args.resize)
if w > 0 and h > 0:
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), trt_bool=str2bool(args.tensorrt))
else:
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), trt_bool=str2bool(args.tensorrt))
logger.debug('cam read+')
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')
s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()




data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))


while True:
    length = recvall(conn,16)
    if length:
        stringData = recvall(conn, int(length))
        data = np.frombuffer(stringData, dtype='uint8') 
        decimg=cv2.imdecode(data,1)
        count=0
        y1=[0.0]
        y=0
        humans = e.inference(decimg, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)

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
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        #cv2.imshow('Image',decimg)
    else:
        print("end")
        break
    key = cv2.waitKey(1)
    if key == 27:
        break
