from threading import Thread
from modules.ChildProcess import ChildProcess
import multiprocessing as mp
import logging
from modules.Evaluation import GPUusge
from collections import defaultdict

log = logging.getLogger()
log.exception("Message for you, sir!")

class ProcessManagerThread(Thread):
    def __init__(self, queue):
        super().__init__()

        self.image_queue_process=None

        self.image_queue = queue
        self.current_process = None  # 현재 만들어져있는 프로세스. None->프로세스 없음

    def run(self):

        gpu=GPUusge(defaultdict(list))
        gpu.start()
        # TODO: DataManager 쓰레드로부터 데이터 받기
        # TODO: 프로세스 불러오거나 생성
        # TODO: 만들어진 (혹은 가져온) 프로세스에게 데이터 전달
        while True:
            try:
                image = self.image_queue.get(timeout=10)
                #print(self.image_queue.qsize())
                if self.current_process == None:
                    self.create_process()
                    print("Create", self.current_process, id(self.current_process))

                else:
                    self.load_process()
                self.execute_process(image)

            except Exception:
                print("Timeout")
                if self.current_process is not None and self.image_queue_process.empty():
                    print("Process stop")
                    self.terminate_process()

                    print("Process Manager", self.current_process, id(self.current_process))
                    self.current_process = None

                    if type(image) is str:
                        print("[System] End Process Manger")
                        print(gpu.getlist())
                        gpu.stop()
                        gpu.join()


                        break

    def execute_process(self,image):
        self.image_queue_process.put(image)


    def load_process(self):
        pass
    def create_process(self):
        q=mp.Queue()
        self.image_queue_process=q
        self.current_process=ChildProcess(q)
        self.current_process.start()


    def terminate_process(self):
        self.current_process.terminate()
        self.current_process.join() # stop 기다리기