import multiprocessing as mp
import time
import socket
import numpy as np
import argparse
import cv2

class Test(mp.Process):
    def __init__(self, image):
        super(Test, self).__init__()
        self.image = image
        args, e,w,h=modle_init()
        self.args=arg
        self.e=e
        self.w=w
        self.h=h

    def run(self):
        from tf_pose.estimator import TfPoseEstimator
        while True:
            decimg=self.image.get()
            if img=="Timeout":
                print("StopProcess")
                break
            humans = self.e.inference(decimg, resize_to_default=(self.w > 0 and self.h > 0), upsample_size=self.args.resize_out_ratio)
            y1=[0.0]
            y=0
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
                    #send_data={"name" :"fall"}
                    #r=requests.post("http://127.0.0.1:5000/http",json=send_data)

            cv2.putText(image,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
      
      """
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
      """

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

# For motion tracking function    
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

def make_arg():
    
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
    return args

def model_init():
    from tf_pose.estimator import TfPoseEstimator
    from tf_pose.networks import get_graph_path, model_wh
    args=make_arg()
    s=time.time()
    print("start tensorflow")
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), trt_bool=str2bool(args.tensorrt))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), trt_bool=str2bool(args.tensorrt))
    print("Timing init",time.time()-s)
    return args, e,w,h

#open pose init 부분 
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
            decimg=cv2.imdecode(data,1)
            receving(decimg,pqueue)            
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