import socket
import threading

class SR:
    def __init__(self, ip = '0.0.0.0', port = 27013, sz = 2048):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((ip, port))
        self.__sz = sz
        self.__lock = threading.Lock()
        self.__datapool = []
        

    def __t_receive(self):
        while True:
            try:
                data, address = self.__socket.recvfrom(self.__sz)
                self.__lock.acquire()
                data = data.decode('UTF-8')
                self.__datapool.append((data, address))
                self.__lock.release()
            except:
                break

    def receive(self):
        t = threading.Thread(target = self.__t_receive, name = 'receiver')
        t.start()

    def send(self, data, address):
        self.__socket.sendto(data.encode('UTF-8'), address)

    def getData(self):
        #self.__lock.acquire()
        if len(self.__datapool) == 0: return None
        data = self.__datapool.pop(0)
        #self.__lock.release()
        return data
    
    def inactive(self):
        self.__socket.close()

