import socket
import sys
import select
import time
import matplotlib.pyplot as plt

class TCP_connection:
    # USB 模式下，机器人默认 IP 地址为 192.168.42.2, 控制命令端口号为 40923
    host = "192.168.42.2"
    port = 40923
    printing = True
    connection = False
    def __init__(self, printing_ = True):
        self.printing = printing_

    def connect(self):# 与机器人控制命令端口建立 TCP 连接
        self.address = (self.host, int(self.port))
        self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.printing:
            print("Connecting_TCP...")

        self.TCP_socket.connect(self.address)
        self.connection = True
        if self.printing:
            print("TCP_Connected!")

    def disconnect(self):# 与机器人控制命令端口断开 TCP 连接
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        if self.printing:
                print("TCP_disconnecting...")
        self.TCP_socket.shutdown(socket.SHUT_WR)
        self.TCP_socket.close()
        if self.printing:
                print("TCP_disconnected!")
    
    def IN(self, message):#检测并向机器发送message
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        if ( str(type(message)) == "<class 'str'>" ) and (message[-1] == ';') :
                if self.printing:
                        print('IN:' , message)
                self.TCP_socket.send(message.encode('utf-8'))
        else:
                if self.printing:
                        print('please input str that ends with ";"')

    def try_get_message(self, timeout=5):#这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        result = ''
        try:
            # 设置超时时间
            ready = select.select([self.TCP_socket], [], [], timeout)
            if ready[0]:
                # 如果有可读数据，接收并解码
                buf = self.TCP_socket.recv(1024)
                result = buf.decode('utf-8')
            else:
                result = 'no_OUT'
        except socket.error as e:
            if self.printing:
                print("Error receiving :", e)
            sys.exit(1)
        return result
    
    def OUT(self, timeout=5):#检测机器回复
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        result = ''
        result = self.try_get(timeout)
        if self.printing:
                print("OUT:", result)
        return result
    
    def IN_OUT(self, message, timeout=5):#检测并向机器发送message，检测机器回复
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        result = ''
        self.IN(message,printing = self.printing)
        result = self.OUT(timeout = timeout,printing = self.printing)
        return result
    def connect_enter_SDK(self, timeout=5):# 与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制
        if not self.connection:
            if self.printing:
                print("You Haven't Connected Yet")
            return
        self.connect_TCP(printing = self.printing)
        self.IN_OUT("command;", timeout = timeout,printing = self.printing)
        self.IN_OUT("quit;", timeout = timeout,printing = self.printing)#以免图传卡住
        self.IN_OUT("command;", timeout = timeout,printing = self.printing)