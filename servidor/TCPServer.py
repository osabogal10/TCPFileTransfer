
import socket, sys, threading, hashlib,time, logging,os
from time import gmtime, strftime

from sys import stderr
from logging import getLogger, StreamHandler, Formatter, DEBUG
from time import sleep
from time import sleep




host, port = '', 9000
SIZE = 2048
hasher = hashlib.md5()




class transfer :

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self):
        num_clients = int(sys.argv[1])
        file_name = sys.argv[2]
        self.mysocket.bind((host, port))
        print(' Server is ready ..')
        self.mysocket.listen(5)
        threads = []
        id_cliente =1
        while num_clients >0:
            conn, addr = self.mysocket.accept()
            size = os.path.getsize(file_name)
            print(' file size : {}'.format(str(size)))
            send_thread = threading.Thread(target = self.send_file, args=(file_name, size, conn, addr, id_cliente ))
            threads.append(send_thread)
            num_clients = num_clients - 1
            id_cliente=id_cliente+1
        for thread in threads:
            thread.start()

    def send_file(self, file_name, size, conn, addr, id_cliente):

        l = getLogger()
        os.makedirs(os.path.dirname('./logs/TCP{}.log'.format(id_cliente)), exist_ok=True)
        logging.basicConfig(format=' %(threadName)s;%(message)s', filename='./logs/TCP{}.log'.format(id_cliente), level=logging.DEBUG)
        sh = StreamHandler(stderr)
        sh.setLevel(DEBUG)
        f = Formatter(' %(message)s')
        sh.setFormatter(f)
        l.addHandler(sh)
        l.setLevel(DEBUG)

        showtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        l.info('%s;%s', 'DATE', showtime)

        l.info('%s;%s', 'FILE_NAME', file_name)
        l.info('%s;%s', 'FILE_SIZE', size)
        l.info('%s;%s', 'CLIENT', id_cliente)
        size = os.path.getsize(file_name)
        i = 0
        bytesSent = 0
        print(' file size : {}'.format(str(size)))

        with open(file_name, 'rb') as file:
            data = file.read(SIZE)
            start_time = time.time()
            conn.send(data)
            while data != bytes(''.encode()):
                #print(data)
                data = file.read(SIZE)
                sent = conn.send(data)
                i = i+1
                bytesSent = bytesSent+sent
                if sent < SIZE:
                    sent = conn.send(b'Fin')
                    print('Fin')
                    break

            elapsed_time = time.time() - start_time
            print(' File sent successfully.')
            l.info('FILE_DELIVERY;SUCCESS')
            l.info('%s;%s', 'BYTES_SENT', bytesSent)
            l.info('%s;%s', 'BYTES_RECEIVED', bytesSent)
            l.info('%s;%s', 'PACKETS SENT', i)
            l.info('%s;%s', 'PACKETS RECEIVED', i)
            l.info('%s;%s', 'ELAPSED_TIME', elapsed_time)
            l.info('-----------------------------------')





Transfer = transfer()