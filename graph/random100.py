import random
import numpy as np
from collections import defaultdict
import pickle

def select_random(prob, X, fps, frame_count, adamm=1):
    total_time = int(frame_count / fps)
    object_time = int(total_time * prob)
    occupy_frame = int(object_time / X)
    tmp = int(X * fps)
    print(tmp)

    if adamm == 1:
        random_list = np.arange(0, int(frame_count - tmp), int(fps)).tolist()
        if prob == 1:
            return random_list, occupy_frame

        random_index = sorted(random.sample(random_list, occupy_frame))
        print("object time", object_time)



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
        print("Random index", random_index)
        return random_index, tmp


def get_time(prob, X):
    fps = 30
    frame_count = 9002

    random_list, occupy = select_random(prob, X, fps, frame_count)

    start_time_list = []
    end_time_list = []

    index = 0

    while index < len(random_list):
        start_time = random_list[index] / fps
        end_time = (random_list[index] + occupy) / fps
        if start_time != -1:
            start_time_list.append(start_time)

        if index < len(random_list) - 1 and end_time == (random_list[index + 1] + occupy) / fps:
            end_time = (random_list[index + 1] + occupy) / fps
            start_time = -1
        else:
            end_time_list.append(end_time)
        index += 1

    print(start_time_list, end_time_list)

    return start_time_list, end_time_list


def get_final_list(adamm, s_t, e_t):
    final_time_list = []
    i = 0
    timeout = 0
    while i < (len(s_t)):
        if i == 0 or timeout == 1:
            print("Start", i)
            final_time_list.append(s_t[i])

        if i < len(s_t)-1 and e_t[i] + 10 < s_t[i + 1]:
            print("Timeout")
            final_time_list.append((e_t[i] + 10))
            timeout = 1
            i += 1
        else:
            print(i)
            i += 1
            timeout = 0
    final_time_list.append(e_t[-1]+1)
    final_time_list = list(map(int, final_time_list))

    return final_time_list


def set_memory(final_time_list):
    Memory = [0.6015791452562977] * 320
    index = 0
    while True:
        # 시작
        if index > len(final_time_list)-1:
            break
        if index % 2 == 0:
            start_time = final_time_list[index]
            end_time = final_time_list[index + 1]
            #print(start_time, end_time)
            Memory[start_time - 2] = 3.2836195011906253
            Memory[start_time - 1] = 7.043489159042486
            for i in range(start_time, end_time + 1):
                Memory[i] = 46.44692317332999
            index += 2
            #print(Memory[end_time+1])
    return Memory


def check_memory(m):
    count = 0
    for i in m:
        if i == 46.44692317332999:
            count += 1

    return count

def write_file(file_name, random_index, prob, X):
    f = open(file_name, 'a+')
    f.write(str(prob) + "," + str(X) + ":")
    for i in random_index:
        f.write(str(i) + " ")
    f.write("\n")
    f.close()


if __name__ == '__main__':
    memory = defaultdict(list)

    prob = [0.1, 0.3, 0.7]
    X = [10, 15, 30]


    """
    s_t, e_t = get_time(prob[2], X[2])
    f_t = get_final_list(True, s_t, e_t)
    m = set_memory(f_t)
    count = check_memory(m)
    #print((m))
    print(f_t, count)
    """
    #f = open("random100.txt", "wb")

    for p in range(0, 3):
        for x in range(0, 3):
            for i in range(0, 100):
                for k in range(0, 2):
                    if k == 0:
                        s_t, e_t = get_time(prob[p], X[x])
                        f_t = get_final_list(True, s_t, e_t)
                        file_name = "random100.txt"
                    else:
                        f_t = [s_t[0], e_t[-1]+1]
                        f_t = list(map(int, f_t))
                        file_name = "random100_non.txt"
                    m = set_memory(f_t)
                    count = check_memory(m)
                    print(k, f_t, count)

                    write_file(file_name, m, prob[p], X[x])
                    memory[prob[p], X[x]].append(m)


    print(memory.keys())
