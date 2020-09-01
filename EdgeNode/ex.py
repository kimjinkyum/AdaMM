import multiprocessing

def motion(data):
    return data+2


if __name__=="__main__":
    pool = multiprocessing.Pool()
    for i in range(10):
        if (i % 2) == 0: # use mod operator to see if "i" is even
            #result.put(i)
            print(pool.apply(motion,(i,)))           
        else:
            if i==5:
                pool.terminate()
                print("terminate")
                pool.join()
                pool=multiprocessing.Pool()
            else:
                continue



