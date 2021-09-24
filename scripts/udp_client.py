#!/usr/bin/bash/python3

from socket import *


class UdpClient:
    """
    A basic implementation of UDP client. This does not support any form of error correction.

    references:
    Socket Programming 101 in Python - Dr. Vinod Vokkarane
    """

    def __init__(self):
        self.server_port = 12000
        self.server_name = "localhost"
        self.client_socket = socket(AF_INET, SOCK_DGRAM)
        self.input_fp = '../data/input_bmp_img_file.bmp'
        self.packet_size = 2048
        self.packets_lst = list()

    def send_message(self, message):
        """
        send message to designated server_address

        :param message: Data to be sent to the server
        :return: # of bytes sent
        """
        # self.client_socket.sendto(message.encode(), (self.server_name, self.server_port))
        self.client_socket.sendto(message, (self.server_name, self.server_port))

    def receive_message(self):
        """
        receive a message from socket using pre-allocated buffer

        :return: returns (message, server_address)
        """
        message = self.client_socket.recvfrom(2048)
        return message[0].decode()

    def make_packets(self):
        """
        Reads in a bmp image file and formats it for server communication

        :return: A matrix of byte arrays
        """
        curr_f = open(self.input_fp, 'rb')
        data = curr_f.read()
        tmp_lst = list()
        # Create desired packet size
        for curr_b in data:
            tmp_lst.append(curr_b)
            if len(tmp_lst) == self.packet_size:
                self.packets_lst.append(bytearray(tmp_lst))
                tmp_lst = list()
        # Append the last packet
        self.packets_lst.append(bytearray(tmp_lst))
        num_packets = len(self.packets_lst)
        # Output file name
        # === Commented out until server code is updated ===
        # self.packets_lst.insert(0, bytearray('output_bmp_img_file.bmp', encoding='utf8'))
        # Number of packets is formatted in little endian
        self.packets_lst.insert(0, bytearray(num_packets.to_bytes(self.packet_size, 'little')))
        curr_f.close()

    def send_packets(self):
        """
        Sends packets one at a time to the server

        :return: None
        """
        for curr_packet in self.packets_lst:
            self.send_message(message=curr_packet)


if __name__ == "__main__":
    client = UdpClient()
    client.make_packets()
    client.send_packets()
