import re
import ipywidgets as widgets
from subprocess import check_output
import threading
def nvidia_smi(options=['-q','-d','MEMORY']):
    return check_output(['nvidia-smi'] + options)

ls=[]

def nvidia_stats():
    out = update_widget()
    out=out.value
    k=out.split("\n")
    used=re.findall("\d+", k[11])[0]
    #print(k[11])#used Memory
    #print(out)
    #print(type(out.value))
    #used=0
    #total = int(out[9].split()[2])
    #units = out[10].split()[3]
    #used = out[10].split()[2]
    ls.append(used)
    print(used)    
    #return used

def update_widget(w=None, new_box=False):
    if w is None:
        w = widgets.Textarea(
            value=nvidia_smi(),
            placeholder='nvidia-smi output',
            width=100,
            disabled=False
        )
        #display(w)
        return w
    else:
        w.value = nvidia_smi()
        if new_box:
            return w
        else:
            return None
nvidia_stats()

def write():
    return ls