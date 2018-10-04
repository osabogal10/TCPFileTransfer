import socket, sys, threading, hashlib,time, logging,os
from time import gmtime, strftime

from sys import stderr
from logging import getLogger, StreamHandler, Formatter, DEBUG
from time import sleep

#configuracion del logger
l = getLogger()
os.makedirs(os.path.dirname('./logs/TCP.log'), exist_ok=True)
logging.basicConfig(format='%(message)s', filename='./logs/TCP.log',  level=logging.DEBUG)
sh = StreamHandler(stderr)
sh.setLevel(DEBUG)
f = Formatter(' %(message)s')
sh.setFormatter(f)
l.addHandler(sh)
l.setLevel(DEBUG)


host, port = '127.0.0.1', 9000
hasher = hashlib.md5()
SIZE=2048

showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
l.info('%s;%s','DATE',showtime)


class recv_data :
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    mysocket.connect((host, port))
    def __init__(self):
        print('Connected successfully')

        filename = self.mysocket.recv(SIZE)
        filesize = self.mysocket.recv(SIZE)
        idCliente = self.mysocket.recv(SIZE)
        start_time = time.time()
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

                break
        elapsed_time = time.time() - start_time
        buf = f.read()
        hasher.update(buf)
        hash_cliente = hasher.hexdigest()
        print('hash cliente: ', hash_cliente)

        l.info('%s;%s', 'FILE_NAME', filename.decode('utf-8'))
        l.info('%s;%s', 'FILE_SIZE', filesize.decode('utf-8'))
        l.info('%s;%s', 'CLIENT', idCliente.decode('utf-8'))

        bytesSent = self.mysocket.recv(64)
        numPack = self.mysocket.recv(64)

        hash_servidor = self.mysocket.recv(64)
        hash_servidor = hash_servidor.decode('utf-8')
        print('hash servidor: ', hash_servidor)
        if hash_servidor == hash_cliente:
            l.info('FILE_DELIVERY;SUCCESS')

        else:
            l.info('FILE_DELIVERY;FAILURE')

        l.info('%s;%s', 'BYTES_SENT', bytesSent.decode('utf-8'))
        l.info('%s;%s', 'BYTES_RECEIVED', str(bytesReceived-3))


        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print('TIME ELAPSED: ', elapsed_time)
        l.info('%s;%s', 'PACKETS SENT', numPack.decode('utf-8'))
        l.info('%s;%s', 'PACKETS RECEIVED', i-1)

        l.info('%s;%s', 'ELAPSED_TIME', elapsed_time)
        l.info('------------------------------')
        logging.shutdown()
        os.rename('./logs/TCP.log', './logs/TCP{}.log'.format(idCliente.decode('utf-8')))




re = recv_data()