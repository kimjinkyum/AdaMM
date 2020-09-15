from threading import Thread


class ProcessManagerThread(Thread):
    def __init__(self, queue):
        super().__init__()

        self.image_queue = queue
        self.current_process = None  # 현재 만들어져있는 프로세스. None->프로세스 없음

    def run(self):
        # TODO: DataManager 쓰레드로부터 데이터 받기
        # TODO: 프로세스 불러오거나 생성
        # TODO: 만들어진 (혹은 가져온) 프로세스에게 데이터 전달
        pass

    def execute_process(self):
        pass

    def create_process(self):
        pass

    def load_process(self):
        pass