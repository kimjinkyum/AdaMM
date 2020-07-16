from webcam import *
import io
import socket
import numpy as np
import cv2
import argparse

    

target="person"

client_socket = socket.socket()
ip_address=" put Edge node IP address" #Edge node Ip address
client_socket.connect((ip_address, 8000))  # ADD IP HERE

connection = client_socket.makefile('wb')

parser = argparse.ArgumentParser(description='Yolo webcam')
parser.add_argument('--camera', type=str, default=0)

args = parser.parse_args()
net,meta=prepare("n","w","m")
cap = cv2.VideoCapture(args.camera)
while True:
    
    ret,img=cap.read()
    if ret is None:
        break
    r=detect(net,meta,img)
    if target in r:
        print(r)
        
        #send frame Socket communication
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', img, encode_param)
        data = np.array(imgencode)
        stringData = data.tostring()
        client_socket.send(str(len(stringData)).ljust(16).encode())
        client_socket.send(stringData)
        for i in r:
            x, y, w, h = i[2][0], i[2][1], i[2][2], i[2][3]
            xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)
            cv2.putText(img, i[0].decode() + " [" + str(round(i[1] * 100, 2)) + "]", (pt1[0], pt1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 0], 4)
        cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
