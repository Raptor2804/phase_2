#!/usr/bin/bash/python3

from socket import *


class UdpEchoServer:
    """
    A basic implementation of a UDP Server. Server class will simply echo any message received from clients

    references:
    Socket Programming 101 in Python - Dr. Vinod Vokkarane
    """

    def __init__(self):
        self.server_port = 12000
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(("localhost", self.server_port))
        print("Server Initialized")

    def run(self):
        """
        Put server into infinite loop wherein it will echo messages received from client in upper case

        :return:
        """
        while True:
            (message, client_address) = self.server_socket.recvfrom(2048)
            modified_message = message.decode().upper()
            print("Message received:{} from {}".format(message, client_address))
            self.server_socket.sendto(modified_message.encode(), client_address)


if __name__ == "__main__":
    server = UdpEchoServer()
    print("Server Running and waiting for connections")
    server.run()
