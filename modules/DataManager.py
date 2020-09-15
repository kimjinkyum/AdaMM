from threading import Thread


class DataManagerThread(Thread):
    def __init__(self, queue):
        super().__init__()

        self.image_queue = queue
        self.server_socket = None

    def run(self):
        # TODO: 데이터 받기
        # TODO: 프로세스 매니저 스레드에 큐로 데이터 전달하기
        pass

    def put_data_to_queue(self):
        # TODO: self.image_queue에 데이터 넣기
        pass