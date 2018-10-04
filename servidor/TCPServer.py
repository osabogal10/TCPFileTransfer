import socket, threading, os, hashlib, sys
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
        size = os.path.getsize(file_name)
        conn.send(file_name.encode('utf-8').zfill(32))
        print(file_name.encode('utf-8'))
        #sleep(0.5)
        conn.send(str(size).encode('utf-8').zfill(32))
        print(str(size).encode('utf-8'))
        #sleep(0.5)
        conn.send(str(id_cliente).encode('utf-8').zfill(32))
        print(str(id_cliente).encode('utf-8'))
        i = 0
        bytesSent = 0
        print(' file size : {}'.format(str(size)))
        with open(file_name, 'rb') as file:
            data = file.read(SIZE)
            conn.send(data)
            ultimo = False
            while data != bytes(''.encode()):
                #print(data)
                if len(data) ==SIZE and len(data)!=0:
                    data = file.read(SIZE)
                    sent = conn.send(data)
                else:
                    data = file.read(SIZE).zfill(SIZE)
                    print('relleno el ultimo')
                    sent = conn.send(data)
                    ultimo = True

                i = i+1
                bytesSent = bytesSent+sent
                if ultimo:
                    fin = b''.zfill(32)
                    sent = conn.send(fin)
                    print(fin)
                    sleep(5)
                    conn.send(str(bytesSent).encode('utf-8').zfill(32))
                    print(str(bytesSent).encode('utf-8').zfill(32))
                    # sleep(0.5)
                    conn.send(str(i).encode('utf-8').zfill(32))
                    print(str(i).encode('utf-8').zfill(32))
                    # sleep(0.5)
                    buf = file.read()
                    hasher.update(buf)
                    hash_servidor = hasher.hexdigest()
                    conn.send(str(hash_servidor).encode('utf-8').zfill(32))
                    print(str(hash_servidor).encode('utf-8').zfill(32))
                    # sleep(0.5)
                    print(' File sent successfully.')
                    break






Transfer = transfer()