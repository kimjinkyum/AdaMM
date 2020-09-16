import threading
from threading import Thread
import re
import ipywidgets as widgets
from subprocess import check_output
import time

class GPUusge(Thread):

    def __init__(self,usage_list):
        super().__init__()
        self.usage_list=usage_list
        self.stop_flag=threading.Event()

    def stop(self):
        self.stop_flag.set()

    def stopped(self):
        return self.stop_flag.isSet()

    def run(self):
        while True:
            if self.stopped():
                return
            self.nvidia_stats()
            time.sleep(1)

    def getlist(self):
        return self.usage_list



    def nvidia_smi(self, options=['-q','-d','MEMORY']):
        return check_output(['nvidia-smi'] + options)

    def nvidia_stats(self):
        out = self.update_widget()
        out = out.value
        k = out.split("\n")
        used = re.findall("\d+", k[11])[0]
        self.usage_list.append(used)
        print("Usage",used)

    def update_widget(self,w=None, new_box=False):
        if w is None:
            w = widgets.Textarea(
                value=self.nvidia_smi(),
                placeholder='nvidia-smi output',
                width=100,
                disabled=False
            )
            # display(w)
            return w
        else:
            w.value = self.vidia_smi()
            if new_box:
                return w
            else:
                return None


