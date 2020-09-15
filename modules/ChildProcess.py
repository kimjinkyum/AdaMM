from multiprocessing import Process

class ChildProcess(Process):
    def __init__(self):
        super().__init__()

    def __del__(self):
        pass

    def run(self):
        pass

    def init_model(self):
        pass