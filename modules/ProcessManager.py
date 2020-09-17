import warnings
warnings.filterwarnings(action="ignore")
from threading import Thread
from modules.ChildProcess import ChildProcess
import multiprocessing as mp

from modules.Evaluation import GPUusge
from collections import defaultdict
import time


class ProcessManagerThread(Thread):
    def __init__(self, queue,adamm):
        super().__init__()
        q=mp.Queue()
        self.adamm=adamm # True --> adamm False -> one-server
        self.image_queue_process=None
        self.start_flag=0
        self.gpu=GPUusge(defaultdict(list))
        self.image_queue = queue
        self.message_queue = q
        self.current_process = None  # 현재 만들어져있는 프로세스. None->프로세스 없음
        self.file_name="One_server_GPU_usage"
        if self.adamm:
            self.file_name="AdaMM_GPU_usage"



    def run(self):
        # TODO: DataManager 쓰레드로부터 데이터 받기
        # TODO: 프로세스 불러오거나 생성
        # TODO: 만들어진 (혹은 가져온) 프로세스에게 데이터 전달
        while True:
            try:
                image = self.image_queue.get(timeout=10)

                if self.current_process == None:
                    if self.start_flag==0:
                        self.gpu.start()
                        self.start_flag = 1
                    self.create_process()
                    print("Create", self.current_process, id(self.current_process))


                else:
                    self.load_process()
                self.execute_process(image)

            except Exception:
                print("Timeout")
                while True:
                    ##print("Queue", self.image_queue_process.qsize())
                    if self.image_queue_process.qsize()==0:
                        break
                if self.current_process is not None:
                    print("Process stop")
                    self.terminate_process()
                    print("Process Manager", self.current_process, id(self.current_process))
                    if type(image) is str:
                        if self.adamm==False:
                            print("asa")
                        print("[System] End Process Manger")
                        time.sleep(1)
                        self.gpu.write_file(self.file_name)
                        self.gpu.stop()
                        self.gpu.join()
                        break




    def execute_process(self,image):
        self.image_queue_process.put(image)


    def load_process(self):
        pass
    def create_process(self):

        q=mp.Queue()
        self.image_queue_process=q
        self.current_process=ChildProcess(q)
        print("Start",time.time())
        self.current_process.start()



    def terminate_process(self):
        if self.adamm:
            self.current_process.terminate()
            self.current_process.join() # stop 기다리기
            self.current_process = None
        else:
            pass