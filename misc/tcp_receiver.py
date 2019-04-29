#!/bin/python3

import sys 
import socket

IP = 'localhost'
PORT = 7000     #GNURadio TCP sink port
SOCKET_BUFFER_SIZE = 1

tcpConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


print('Connecting to:', IP,':', PORT)
tcpConnection.connect((IP, PORT))
print('TCP Connection Sucessfull')   # Program execution is aborted if socket doesn't connect

while(True):
    data = tcpConnection.recv(SOCKET_BUFFER_SIZE)
    print(data)


tcpConnection.close()    




#   # 13 s.send(MESSAGE)
# data = tcpConnection.recv(TCP_BUFFER_SIZE)

# tcpConnection.close()

# # tcpConnection = TCPClient(IP, PORT)




