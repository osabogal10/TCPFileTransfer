import socket, sys, threading, hashlib

from time import sleep

host, port = '127.0.0.1', 9000
hasher = hashlib.md5()


class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))
    print('conectado (?')
    def __init__(self):
        data = self.mysocket.recv(1024)
        f = open('newfile.jpg', 'wb+')
        while data != bytes(''.encode()):
            #print(data)
            f.write(data)
            data = self.mysocket.recv(1024)
        buf = f.read()
        hasher.update(buf)
        print('hash: ', hasher.hexdigest())



re = recv_data()