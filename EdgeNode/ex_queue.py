import multiprocessing as mp
import time
import socket
import numpy as np
#import socket.timeout as TimeoutException
class Test(mp.Process):
  def __init__(self, image):
    super(Test, self).__init__()
    self.image = image
    
  def run(self):
      #Tensorflow 모델 불러오기
      while True:
          start_time=time.time()
          img=self.image.get()
          #time.sleep(1)
          print(img)
          # motion tracking 진행
          if img=="Timeout":
              print("StopProcess")
              #self.terminate()
              break
          #print("I'm the process with id: {}".format(img))

def receving(img,queue):
    queue.put(img)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

if __name__ == '__main__':
    pqueue=mp.Queue()
    global processes
    processes=Test(pqueue)
    HOST='127.0.0.1' #Edge Your IP address
    PORT=8000 
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')
    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')
    conn,addr=s.accept()
    conn.settimeout(2)
    #processes.start()
    flag=0
    j=0
    start_time=0
    while True:
        if flag==0 and not processes.is_alive():
            flag=1
            pqueue=mp.Queue()
            processes=Test(pqueue)
            processes.start()
            print("init")
        try:
            length = recvall(conn,16)
        except socket.timeout:
            print("Waiting")
            if flag==1:
                flag=0
                print("stop process")
                receving("Timeout",pqueue)
                processes.terminate()     
            continue

        if length:
            stringData = recvall(conn, int(length))
            data = np.frombuffer(stringData, dtype='uint8')
            receving(data[0],pqueue)            
        else:
            print("esle")
            break
        
    print("end python")
    
"""
    while True:
        length = recvall(conn,16)
        start_time=time.time()
        if flag==0:
            flag=1
            processes=Test(pqueue)
            processes.start()
        if time.time()-start_time>2:
            print("stopstop")
            receving("Timeout",pqueue)
            processes.terminate()
            flag=0
        data=conn.recv(1024)
        print(time.time()-start_time)
        data=data.decode()
        print(data)
        if data:
            #print(data)
            receving(data,pqueue)
        if not data:
            break
    """         


  #processes = Test(1), Test(2), Test(3), Test(4)
  #[p.start() for p in processes]