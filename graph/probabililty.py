import socket
import argparse
import random
import numpy as np
import time
import cv2


# Prob : 오브젝트가 총 % 출현
# X : object 가 출현 했을 때 몇 frame (몇 초 나오는지)
def select_random(prob, X, fps, frame_count, adamm=True):
    total_time = int(frame_count / fps)
    object_time = int(total_time * prob)
    occupy_frame = int(fps * X)
    print(occupy_frame)

    if adamm:
        random_list = np.arange(0, int(frame_count), 30).tolist()

        random_index = sorted(random.sample(random_list, int(object_time * fps / occupy_frame)))
        print(object_time)

        print(random_index)
        """
        while True:
            count = 0
            for i in range(len(random_index) - 1):
                if random_index[i + 1] <= random_index[i] + occupy_frame:
                    #random_index = sorted(random.sample(random_list, int(object_time * fps / occupy_frame)))
                    random_index[i+1] = random_index[i] + occupy_frame+i
                    print("in")
                    count += 1

            if count == 0:
                print(random_index)
                break
        write_file(random_index, prob, X)
        """
        return random_index, occupy_frame
    else:
        random_index = read_file(prob, X)
        return random_index, occupy_frame


def read_file(prob, X):
    f = open("../data/random_list.txt", 'r')
    result = []
    while True:
        line = f.read()
        if line == "":
            f.close()
            break

        else:
            lines = line.split(":")
            probs = lines[0].split("_")[0]
            Xs = lines[0].split("_")[1]

            if float(probs) == prob and float(Xs) == X:
                return store_list(lines[1].split("\n")[0])


def store_list(line):
    result = []
    lines = line.split(" ")
    for i in lines:
        result.append(int(i))

    return result


def write_file(random_index, prob, X):
    f = open("../data/random_list.txt", 'a+')
    f.write(str(prob) + "_" + str(X) + ":")
    for i in random_index:
        f.write(str(i) + " ")
    f.write("\n")
    f.close()


def send(selected_index, occupy_frame, frame_count, fps, video_path):
    cam = cv2.VideoCapture(video_path)
    cam.set(cv2.CAP_PROP_FPS, fps)
    i = 0
    j = 0
    k = 0
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
                print(i)
                while True:
                    if j == 29:
                        while True:
                            if time.time() - prev_time > 1:
                                break
                    if time.time() - prev_time > 1:
                        frame_index += 1
                        j = 0
                        i += 30
                        print(time.time() - prev_time)
                        break
                    cam.set(cv2.CAP_PROP_POS_FRAMES, selected_index[frame_index] + j)

                    # Send 부분
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    result, imgencode = cv2.imencode('.jpg', img, encode_param)
                    data = np.array(imgencode)
                    stringData = data.tostring()

                    #client_socket.send(str(len(stringData)).ljust(16).encode())
                    #client_socket.send(stringData)

                    j += 1
            else:
                prev_time1 = time.time()
                while True:
                    if k==29:
                        i+=30
                        while True:
                            if time.time()-prev_time1 > 1:
                                break
                    if time.time()-prev_time1>1:
                        print(i)
                        print("Waiting", time.time()-prev_time1)
                        k =0
                        break

                    k += 1
        else:
            prev_tim2 =time.time()
            while True:
                if time.time()-prev_tim2 >1:
                    i += 30
                    break;


        if i == frame_count:
            if time.time() - start_time < frame_count / fps:
                while True:
                    if time.time() - start_time > frame_count / fps:
                        break

    print(time.time() - start_time)
    print(i)


if __name__ == '__main__':
    client_socket = socket.socket()

    parser = argparse.ArgumentParser(description="Send based object probability")
    #video_path = "video/test2.mp4"
    video_path = "../data/test2.mp4"
    parser.add_argument("--prob", type=float, default=0.8)
    parser.add_argument("--X", type=float, default=1)
    parser.add_argument("--camera", type=str, default=video_path)
    parser.add_argument("-adamm", type=bool, default=True)
    args = parser.parse_args()

    cam = cv2.VideoCapture(args.camera)
    frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cam.get(cv2.CAP_PROP_FPS)
    total_time = int(frame_count / fps)

    print("frame_count", frame_count)
    print("total_time", total_time)
    random_index, occupy_frame = select_random(args.prob, args.X, fps, frame_count, args.adamm)
    #ip_address = "127.0.0.1"  # Edge node Ip address
    #client_socket.connect((ip_address, 8000))  # ADD IP HERE

    #connection = client_socket.makefile('wb')
    send(random_index, occupy_frame, frame_count, fps, video_path)