# 확률값에 따라 데이터 전송

import numpy as np
import time
import cv2
import argparse
import random


def cam_read(flag=False):
    video_path = "../data/example_video.mp4"
    cam = cv2.VideoCapture(video_path)

    frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cam.get(cv2.CAP_PROP_FPS)
    total_time = frame_count / fps

    return fps, total_time


def select_random(args):
    fps, total_time = cam_read()
    print(total_time)
    object_time = int(total_time * (args.prob / 100))

    random_list = np.arange(int(total_time)).tolist()
    random_time = sorted(random.sample(random_list, object_time))

    print(object_time)
    print(random_time)

    random_index = np.array(random_time) * fps

    print(random_index)
    return random_index, fps


def send(selected_index, fps,  video_path):
    cam = cv2.VideoCapture(video_path)
    index = 0
    count = 0
    sub_count = 0
    start_time = time.time()
    while True:
        ret, img = cam.read()
        if img is None:
            break

        if index < len(selected_index) and count == selected_index[index]+sub_count:

            if sub_count == 0:
                start_time = time.time()
                print("Select start", start_time)

            if sub_count >= fps:
                index += 1
                sub_count = 0

                print("Select end", time.time()-start_time)
                continue

            print("Selected",selected_index[index]+sub_count)
            cv2.imshow('tf-pose-estimation result', img)
            _ = 0xFF & cv2.waitKey(1)

            sub_count += 1
            count += 1

        else:
            count += 1
            sub_count = 0

    print(count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send based object probability")
    parser.add_argument("--prob", type=float, default=100)
    args = parser.parse_args()

    random_time, fps = select_random(args)
    video_path = "../data/example_video.mp4"

    send(random_time, fps, video_path)

