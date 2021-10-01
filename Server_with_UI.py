#!/usr/bin/bash/python3

from socket import *
import io
import os
import PySimpleGUI as sg
from tkinter import *



class ClientInstance:
    """
    Client instance will store the packets received from a client, and when the transfer is complete it will store a
    copy of the file that was transferred by the client
    """

    # TODO add in filename to the constructor and parser
    def __init__(self, ip_address, port_number):
        self.ip_address = ip_address
        self.port_number = port_number
        self.number_of_packets = -1
        self.data = []
        # === I believe the server doesn't account for the file name yet ===
        self.filename = "Received_File.bmp"


class UdpFileTransferServer:
    """
    A basic implementation of a UDP Server. Server will receive a file from the client and store it locally
    references:
    Socket Programming 101 in Python - Dr. Vinod Vokkarane
    """

    def __init__(self):
        self.server_port = 12000
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(("localhost", self.server_port))
        self.client_list = []
        self.most_recent_client = "NO CLIENT"
        self.set_filename = ''
        self.data = []
        self.num_incoming_packets = 0
        print("Server Initialized")


    def rdt_rcv(self):
        """
        Put server into infinite loop wherein it will receive packets from clients and save corresponding images to disk
        reference:
        https://stackoverflow.com/questions/16705861/check-if-instance-present-in-list
        """
        while True:
            # Maximum buffer size of 2048
            (message, client_address) = self.server_socket.recvfrom(2048)
            self.extract(message, client_address)

            # print("Received packet from {}".format(client_address))
            # ACK package not required here
            # self.server_socket.sendto(modified_message.encode(), client_address)

    def client_list_contains(self, client):
        for i in range(len(self.client_list)):
            if self.client_list[i].ip_address == client.ip_address:
            #self.client_list[i].port_number == client.port_number:
                return True, i
        return False, -1

    def extract(self, message, client_address):
        self.data.append(message)
        # Decoding the first byte array to extract number of packets "
        if len(self.data) == 1:
            self.num_incoming_packets = int.from_bytes(self.data[0], 'little')
        """
        check if all the packets(message) have been received by the server
        The second packet contains the filename, that it needs to be saved with
        """
        if len(self.data) == self.num_incoming_packets + 2:
            #Decoding the message to extract the file name"
            self.set_filename = self.data[1].decode('utf-8')
            self.deliver_data(client_address)


    def deliver_data(self, client_address):
        f = open(self.set_filename, 'wb')
        # Writing all the data from self.data into a file, except for first 2 packet message"
        for i in range(2, len(self.data)):
            f.write(bytes(self.data[i]))
        f.close()
        print("Finished receiving {} packets".format(self.num_incoming_packets) )
        print("File name {}".format(self.set_filename))
        #A new client instance created with the client address, IP address and port number"
        client = ClientInstance(client_address[0], client_address[1])
        # Checking if it exists in the client list"
        stored_location = self.client_list_contains(client)
        """
        If this client exists in the client list, we update the information sent through this
        client in its object, including data, num_of_packets and filename
        Else, we can keep updating the new client Instance with the file name, 
        number of packets and the data. Also the client object is added to the end of the client_list 
        """
        if stored_location[0]:
            print("Client previously connected, at client list {}".format(stored_location[1]) )
            self.client_list[stored_location[1]].data = self.data
            self.client_list[stored_location[1]].filename = self.set_filename
            self.client_list[stored_location[1]].num_of_packets = self.num_incoming_packets
        else:
            client.data = self.data
            client.filename = self.set_filename
            client.number_of_packets = self.num_incoming_packets
            self.client_list.append(client)
            print("{} new client added".format(client.ip_address))
            self.most_recent_client = self.client_list[-1]
            # clear the data field where the packets were stored initially
        self.data.clear()
    #     #############################################
    #     layout = [
    #         [sg.Image(key="-IMAGE-")],
    #         [
    #             sg.Text("Image File"),
    #             sg.Input(size=(25, 1), key="-FILE-"),
    #             sg.FileBrowse(file_types="*.bmp"),
    #             sg.Button("Load Image"),
    #         ],
    #     ]
    #     window = sg.Window("Image Viewer", layout)
    #     while True:
    #         event, values = window.read()
    #         if event == "Exit" or event == sg.WIN_CLOSED:
    #             break
    #         if event == "Load Image":
    #             filename = values["-FILE-"]
    #             if os.path.exists(filename):
    #                 image = Image.open(values["-FILE-"])
    #                 image.thumbnail((400, 400))
    #                 bio = io.BytesIO()
    #                 image.save(bio, format="PNG")
    #                 window["-IMAGE-"].update(data=bio.getvalue())
    #     window.close()
    #
    # ################################################

if __name__ == "__main__":
    server = UdpFileTransferServer()
    print("Server Running and waiting for connections")
    server.rdt_rcv()
