import socket
import argparse
import cv2
import time
import numpy as np

def frame_differencing(prev_frame, current_frame, threshold):
    prev_frame1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    current_frame1 = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    diff = abs(prev_frame1-current_frame1)

    diff_result = len(np.where((diff.ravel()) > threshold)[0])
    if diff_result > len(diff.ravel()) * 0.5:
        print("Different")
        return current_frame


if __name__ == '__main__':
    client_socket = socket.socket()

    parser = argparse.ArgumentParser(description="Send based object probability")
    video_path = "C:\\Users\\kimo1\\Downloads\\video3.mp4"
    parser.add_argument("--video_path", type=str, default=video_path)
    parser.add_argument("--FD", type=int, default=0)
    parser.add_argument("--th", type=float, default=35)

    args = parser.parse_args()

    frame_list = [0, 1800, 5400, 7200, 7500, 8400]

    cam = cv2.VideoCapture(args.video_path)
    frame_index = 0
    object_index = 0
    fps_time = time.time()
    start_time = time.time()
    ret, img = cam.read()
    frame_p = img
    while True:
        if ret is None:
            break
        if object_index < len(frame_list)-1:
            if frame_list[object_index] <= frame_index <= frame_list[object_index + 1]:
                if frame_index == frame_list[object_index]:
                    sub_start_time = time.time()
                    print("Start time", sub_start_time-start_time)

                if frame_index == frame_list[object_index+1]:
                    print("End time", time.time()-sub_start_time)
                    object_index += 2

                if args.FD == 1:
                    send_frame = frame_differencing(frame_p, img, args.th)
                else:
                    send_frame = img

                if send_frame is not None:

                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    result, imgencode = cv2.imencode('.jpg', send_frame, encode_param)
                    data = np.array(imgencode)
                    stringData = data.tostring()

                    client_socket.send(str(len(stringData)).ljust(16).encode())
                    client_socket.send(stringData)


        while frame_index % 30 == 0 and frame_index > 0:
            if time.time()-fps_time > 1:
                fps_time = time.time()
                break
        if frame_index % 100 == 0:
            print(frame_index)
            print(time.time()-start_time)

        frame_p = img.copy()
        ret, img = cam.read()
        frame_index += 1



