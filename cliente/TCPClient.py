import socket, sys, threading, hashlib,time, logging,os
from time import gmtime, strftime

from sys import stderr
from logging import getLogger, StreamHandler, Formatter, DEBUG
from time import sleep


host, port = '172.24.101.228', 9000
#host, port = '127.0.0.1', 9000
hasher = hashlib.md5()
SIZE=2048

class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))
    def __init__(self):
        print('Connected successfully')
        start_time = time.time()
        data = self.mysocket.recv(SIZE)
        #hash_servidor = hash_servidor
        i=0
        bytesReceived=0

        with open(sys.argv[1], 'wb+') as f:
            while data != bytes(''.encode()):
                #print(data)
                f.write(data)
                data = self.mysocket.recv(SIZE)
                bytesReceived=bytesReceived+len(data);
                i=i+1
                if data == b'Fin' :
                    print('Fin de archivo')
                    break
            elapsed_time = time.time() - start_time

            buf = f.read()
            hasher.update(buf)
            hash_cliente = hasher.hexdigest()
            print('hash cliente: ', hash_cliente)


            print('exito')



re = recv_data()