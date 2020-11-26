import socket
import argparse
import random
import numpy as np
import time
import cv2


# Prob : 오브젝트가 총 % 출현
# X : object 가 출현 했을 때 몇 frame (몇 초 나오는지)
def select_random(prob, X, fps, frame_count):
    # fps, total_time = cam_read()
    # print(total_time)
    total_time = int(frame_count / fps)
    object_time = int(total_time * prob)
    occupy_frame = int(fps * X)
    print(occupy_frame)

    random_list = np.arange(0, int(frame_count), 3).tolist()

    random_index = sorted(random.sample(random_list, int(object_time * fps / occupy_frame)))
    print(object_time)

    print(random_index)
    while True:
        count = 0
        for i in range(len(random_index) - 1):
            if random_index[i + 1] < random_index[i] + occupy_frame:
                random_index = sorted(random.sample(random_list, int(object_time * fps / occupy_frame)))
                count += 1
        if count == 0:
            break

    return random_index, occupy_frame


def send(selected_index, occupy_frame, frame_count, fps, video_path):
    cam = cv2.VideoCapture(video_path)
    cam.set(cv2.CAP_PROP_FPS, fps)
    i = 0
    j = 0
    start_time = time.time()
    frame_index = 0
    start_time = time.time()
    while True:
        ret, img = cam.read()
        if i == 0:
            start_time = time.time()
        if img is None:
            break
        if time.time() - start_time > frame_count / fps:
            break
        if frame_index < len(selected_index):
            if i == selected_index[frame_index]:
                prev_time = time.time()
                while True:
                    if time.time() - prev_time > 1:
                        frame_index += 1
                        j = 0
                        print(time.time() - prev_time)
                        break
                    cam.set(cv2.CAP_PROP_POS_FRAMES, selected_index[frame_index] + j)

                    # Send 부분
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    result, imgencode = cv2.imencode('.jpg', img, encode_param)
                    data = np.array(imgencode)
                    stringData = data.tostring()

                    client_socket.send(str(len(stringData)).ljust(16).encode())
                    client_socket.send(stringData)

                    i += 1
                    j += 1
            else:
                i += 1
        else:
            i += 1

        if i == frame_count:
            if time.time() - start_time < frame_count / fps:
                while True:
                    if time.time() - start_time > frame_count / fps:
                        break

    print(time.time() - start_time)
    print(i)


if __name__ == '__main__':
    client_socket = socket.socket()

    ip_address = "127.0.0.1"  # Edge node Ip address
    client_socket.connect((ip_address, 8000))  # ADD IP HERE

    connection = client_socket.makefile('wb')

    parser = argparse.ArgumentParser(description="Send based object probability")
    video_path = "C://Users//kimo1//OneDrive//바탕 화면//dev//data//t1.mp4"

    parser.add_argument("--prob", type=float, default=0.7)
    parser.add_argument("--X", type=float, default=1)
    parser.add_argument("--camera", type=str, default=video_path)
    args = parser.parse_args()

    cam = cv2.VideoCapture(args.camera)
    frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cam.get(cv2.CAP_PROP_FPS)
    total_time = int(frame_count / fps)

    print("frame_count", frame_count)
    print("total_time", total_time)
    random_index, occupy_frame = select_random(args.prob, args.X, fps, frame_count)
    send(random_index, occupy_frame, frame_count, fps, video_path)
