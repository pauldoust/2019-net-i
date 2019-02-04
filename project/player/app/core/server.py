# from project.player.app.utilites.netutils import Netutils
import sys
sys.path.insert(0,'..')
from utilites.netutils import *

import socket as sock
from threading import Thread
import queue

class Server:
    """docstring for Tracker"""
    def __init__(self, ip, port):
        # try:
        #     self.ip = ip
        #     self.port = port
        #     self.peers = dict()
        #     self.run()
        # except Exception as e:
        #     print("exit", e)
        self.ip = ip
        self.port = port
        self.peers = dict()
        self.run()

    def handler(self, socket):
        # def handle():
        raise NotImplementedError("Please Implement this method in child class")
        # def handle2():
        #     l = netutils.read_line(socket)
        #     while l is not None:
        #         print("RECEIVED:", l)
        #         l = netutils.read_line(socket)

        # t = Thread(target=handle2)
        # return t

    def run(self):
        print("server initializing..")
        self.handle_acceptall().start()



    def handle_acceptall(self):
        def handle():
            server_socket = sock.socket()
            server_socket.bind((self.ip, self.port))
            server_socket.listen()
            print(server_socket)
            while  True:
                # print("waiting connection")
                socket, addr = server_socket.accept()
                # print("connection accepted !")
                self.handler(socket).start()


        t = Thread(target=handle())
        return t


# if __name__== "__main__":
#     s = Server("localhost", 9999)
