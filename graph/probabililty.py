import socket
import argparse
import random
import numpy as np
import time
import cv2



def select_random(prob, X, fps, frame_count, adamm):
    total_time = int(frame_count / fps)
    object_time = int(total_time * prob)
    occupy_frame = int(object_time / X)
    tmp = int(X*fps)
    print(occupy_frame)

    if adamm==1:
        random_list = np.arange(0, int(frame_count), int(fps)).tolist()
        #print(random_list)
        if prob == 1:
            write_file(random_list, prob, X)
            return random_list, occupy_frame

        random_index = sorted(random.sample(random_list, occupy_frame))
        print("object time", object_time)

        print("Random index", random_index)
        
        while True:
            count = 0
            for i in range(len(random_index) - 1):
                if random_index[i + 1] < random_index[i] + tmp:
                    random_index[i + 1] = random_index[i] + tmp
                    count += 1

            if count == 0:
                if random_index[-1] > frame_count - tmp:
                    random_index = sorted(random.sample(random_list, occupy_frame))
                    count = 1
                    print("in")
                else:
                    break
       
        
        write_file(random_index, prob, X)
        return random_index, occupy_frame
    else:
        print("Read")
        random_index = read_file(prob, X)
        return random_index, occupy_frame





def read_file(prob, X):
    f = open("../data/random_list1.txt", 'r')
    result = []
    i=0
    line = f.read()
    line = ''.join(line)
    line = line.split("\n")
    #print("line", line)
    #line = line[0]
    while True:    
        if line =="":
            continue
        #print(line)
        
        
        lines = line[i].split(":")
        #print(lines)
        probs = lines[0].split("_")[0]
        Xs = lines[0].split("_")[1]
        print(probs,Xs)
        if float(probs) == prob and float(Xs) == X:
            #print(lines[1].split("\n")[0])
            return store_list(lines[1].split("\n")[0])
        i+=1


def store_list(line):
    result = []
    lines = line.split(" ")
    print(lines)
    for i in lines:
        if i=="":
            continue
        result.append(int(i))

    return result


def write_file(random_index, prob, X):
    f = open("../data/random_list.txt", 'a+')
    f.write(str(prob) + "_" + str(X) + ":")
    for i in random_index:
        f.write(str(i) + " ")
    f.write("\n")
    f.close()


def send(selected_index, occupy_frame, frame_count, fps, video_path,X,p):
    cam = cv2.VideoCapture(video_path)
    cam.set(cv2.CAP_PROP_FPS, fps)
    i = 0
    j = 0
    k = 0
    waiting_time = occupy_frame / fps
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
                print(p,": Ready for send")
                while True:
                    
                    if time.time() - prev_time > X:
                        frame_index += 1
                        j = 0
                        i +=int(fps*X)
                        print(time.time() - prev_time)
                        break
                    cam.set(cv2.CAP_PROP_POS_FRAMES, selected_index[frame_index] + j)
                    
                    
                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                    result, imgencode = cv2.imencode('.jpg', img, encode_param)
                    data = np.array(imgencode)
                    stringData = data.tostring()

                    client_socket.send(str(len(stringData)).ljust(16).encode())
                    client_socket.send(stringData)
                    #print(send)
                    j += 1 
            else:
                prev_time1 = time.time()
                while True:    
                    if time.time()-prev_time1>1:
                        i+=fps
                        print(p,": " ,i, time.time()-prev_time1)
                        #k =0
                        break
        else:
            prev_tim2 =time.time()
            while True:
                if time.time()-prev_tim2 > 1:
                    i+=fps
                    print(p,": ",i ,time.time()-prev_tim2)
                    break;


        if i == frame_count:
            if time.time() - start_time < frame_count / fps:
                while True:
                    if time.time() - start_time > frame_count / fps:
                        print("End send")
                        break

    print(time.time() - start_time)
    print(i)


if __name__ == '__main__':
    client_socket = socket.socket()

    parser = argparse.ArgumentParser(description="Send based object probability")
    video_path = "video/video2.mp4"
    #video_path = "../data/video2.mp4"
    parser.add_argument("--prob", type=float, default=0.5)
    parser.add_argument("--X", type=float, default=5)
    parser.add_argument("--camera", type=str, default=video_path)
    parser.add_argument("--adamm", type=float, default=1)
    args = parser.parse_args()
    print(args.adamm)
    cam = cv2.VideoCapture(args.camera)
    frame_count = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cam.get(cv2.CAP_PROP_FPS)
    total_time = int(frame_count / fps)

    print("frame_count", frame_count)
    print("total_time", total_time)
    print("X, prob", args.X, args.prob)
    random_index, occupy_frame = select_random(args.prob, args.X, fps, frame_count, args.adamm)
    ip_address = "127.0.0.1"  # Edge node Ip address
    client_socket.connect((ip_address, 8100))  # ADD IP HERE

    connection = client_socket.makefile('wb')
    send(random_index, occupy_frame, frame_count, fps, video_path,args.X,args.prob)
