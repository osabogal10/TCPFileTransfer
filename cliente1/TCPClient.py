import socket, sys, threading, hashlib,time
from time import gmtime, strftime

from time import sleep

host, port = '127.0.0.1', 9000
hasher = hashlib.md5()
SIZE=1024

class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))
    def __init__(self):
        start_time = time.time()
        filename = self.mysocket.recv(SIZE)
        idCliente = self.mysocket.recv(SIZE)
        data = self.mysocket.recv(SIZE)
        i=0
        bytesReceived=0
        f = open(filename.decode('utf-8'), 'wb+')
        while data != bytes(''.encode()):
            #print(data)
            f.write(data)
            data = self.mysocket.recv(SIZE)
            bytesReceived=bytesReceived+len(data);
            i=i+1
            if data == b'Fin' :
                print('Fin de la wea')
                break
        buf = f.read()
        hasher.update(buf)
        hash_cliente = hasher.hexdigest()

        print('hash: ', hasher.hexdigest())
        print('FILE NAME: ', filename.decode('utf-8'))
        print('CLIENTE: ', idCliente.decode('utf-8'))
        bytesSent = self.mysocket.recv(SIZE)
        print('SENT BYTES: ', bytesSent.decode('utf-8'))
        print('RECEIVED BYTES: ', bytesReceived-3)
        numPack = self.mysocket.recv(SIZE)
        print('PACKETS SEND: ', numPack.decode('utf-8'))
        print('PACKETS RECEIVED: ', i-1)
        hash_servidor = self.mysocket.recv(SIZE)
        hash_servidor = hash_servidor.decode('utf-8')
        if hash_servidor == hash_cliente:
            print('FILE DELIVERY: SUCCESS')
        else:
            print('FILE DELIVER: FAILURE')

        elapsed_time = time.time() - start_time
        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print('TIME ELAPSED: ', elapsed_time)
        print('DATE: ', showtime)


re = recv_data()