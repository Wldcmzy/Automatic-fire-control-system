import socket
import threading
from typing import Tuple

class SR:
    def __init__(self, ip = '0.0.0.0', port = 27013, sz = 2048) -> None:
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((ip, port))
        self.__sz = sz
        self.__lock = threading.Lock()
        self.__datapool = []
        

    def __t_receive(self) -> None:
        '''接收消息, 应该放到单独的线程中'''
        while True:
            try:
                data, address = self.__socket.recvfrom(self.__sz)
                self.__lock.acquire()
                data = data.decode('UTF-8')
                self.__datapool.append((data, address))
                self.__lock.release()
            except:
                break

    def receive(self) -> None:
        '''开启消息接收的方法'''
        t = threading.Thread(target = self.__t_receive, name = 'receiver')
        t.start()

    def send(self, data, address) -> None:
        '''发送消息'''
        self.__socket.sendto(data.encode('UTF-8'), address)

    def getData(self) -> Tuple[str, Tuple[str, int]]:
        '''
        从消息队列中提取一条最早的数据
        return : (msg, (ip, port))
        '''
        #self.__lock.acquire()
        if len(self.__datapool) == 0: return None
        data = self.__datapool.pop(0)
        #self.__lock.release()
        return data
    
    def inactive(self):
        self.__socket.close()

