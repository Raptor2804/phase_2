#!/usr/bin/bash/python3

from socket import *
import os
import PySimpleGUI as sg

sg.theme('Dark Blue 3')


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
        self.input_fp = 'input_bmp_img_file.bmp'
        self.packet_size = 2048
        self.packets_lst = list()

    def udt_send(self, message):
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

    def make_pkt(self):
        """
        Reads in a file and formats it for server communication
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
        # Number of packets is formatted in little endian
        self.packets_lst.insert(0, bytearray(num_packets.to_bytes(self.packet_size, 'little')))
        print(num_packets)
        # Output file name
        # === Commented out until server code is updated ===
        self.packets_lst.insert(1, bytearray('Pknaskf.bmp', encoding='utf8'))
        curr_f.close()

    def rdt_send(self):
        """
        Sends packets one at a time to the server
        :return: None
        """
        for curr_packet in self.packets_lst:
            self.udt_send(message=curr_packet)

def send():
    ############################################################
                #UI code
    layout = [[sg.Text('Sending file')],

              [sg.ProgressBar(1, orientation='h', size=(20, 20), key='progress')],
              [sg.Cancel()]]
    window = sg.Window('Sending file', layout)
    progress_bar = window['progress']
    # loop that would normally do something useful
    # print(num_packets)
    for i in range(1600):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        if event == 'Cancel' or event == None:
            break
        # update bar with loop value +1 so that bar eventually reaches the maximum
        progress_bar.update_bar(i + 1, 1600)
    # done with loop... need to destroy the window as it's still open
    window.close()


    client = UdpClient()
    client.make_pkt()
    client.rdt_send()


if __name__ == "__main__":
    client = UdpClient()
    global num_packets
    file_path = ''
    """
    Window 1 will be created
    """
    layout = [[sg.Text("Choose a file: "), sg.Input(), sg.FileBrowse(key="-IN-")], [sg.Button("Send", key=send)]]
    window = sg.Window('Client', layout, size=(600, 150))
    event, values = window.read()
    filepath = values["-IN-"]
    send()
    client.make_pkt()
    client.rdt_send()