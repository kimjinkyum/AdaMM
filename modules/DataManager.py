from threading import Thread
import numpy as np
import cv2

class DataManagerThread(Thread):
    def __init__(self, queue,sock):
        super().__init__()

        self.image_queue = queue
        self.server_socket = sock


    def run(self):
        # TODO: 데이터 받기
        while True:
            length = self.recvall(16)
            if length:
                stringData = self.recvall(int(length))
                data = np.frombuffer(stringData, dtype='uint8')
                # TODO: 프로세스 매니저 스레드에 큐로 데이터 전달하기
                self.put_data_to_queue(data)

                #img=cv2.imdecode(data,1) // For image


    def recvall(self,count):
        #데이터 받아오는 함수
        buf = b''
        while count:
            newbuf = self.server_socket.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def put_data_to_queue(self,image):
        # TODO: self.image_queue에 데이터 넣기
        self.image_queue.put(image)
