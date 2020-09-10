import socket
import time
import numpy as np
client_socket = socket.socket()

ip_address="127.0.0.1" #Edge node Ip address
client_socket.connect((ip_address, 8000))  # ADD IP HERE

connection = client_socket.makefile('wb')
i=0
a=""
while True:
    data = np.array(i)
    stringData = data.tostring()
    #client_socket.send(data.encode())
    time.sleep(0.5)
    if i==5:
        #client_socket.send(str(len(a)).ljust(16).encode())
        time.sleep(5)
    else:
        client_socket.send(str(len(stringData)).ljust(16).encode())
        client_socket.send(stringData)

    if i>10:
        break
    i+=1
