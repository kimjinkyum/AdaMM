from multiprocessing import Process


class ChildProcess(Process):
    def __init__(self):
        super().__init__()

    def __del__(self):
        pass

    # Start 혹은 run 메소드 실행 시
    def run(self):
        print("child process")
        pass

    def init_model(self):
        pass
