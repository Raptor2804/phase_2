#!/usr/bin/bash/python3

from socket import *


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
        self.filename = "DEFAULT_FILE.txt"


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
        print("Server Initialized")

    def run(self):
        """
        Put server into infinite loop wherein it will receive packets from clients and save corresponding images to disk
        
        reference:
        https://stackoverflow.com/questions/16705861/check-if-instance-present-in-list
        """
        while True:
            # Maximum buffer size of 2048
            (message, client_address) = self.server_socket.recvfrom(2048)
            self.parse_message_and_update(message, client_address)

            # print("Received packet from {}".format(client_address))
            # ACK package not required here
            # self.server_socket.sendto(modified_message.encode(), client_address)

    def client_list_contains(self, client):
        for i in range(len(self.client_list)):
            if self.client_list[i].ip_address == client.ip_address and \
                    self.client_list[i].port_number == client.port_number:
                return True, i
        return False, -1

    def parse_message_and_update(self, message, client_address):
        client = ClientInstance(client_address[0], client_address[1])
        # if the client has already connected before update that instance
        stored_location = self.client_list_contains(client)

        # client already exists then update its data, otherwise init the structure for it
        if stored_location[0]:

            # TODO Debug
            # print("{}:{} has already been found".format(client.ip_address, client.port_number))
            self.client_list[stored_location[1]].data.append(message)
            # TODO Debug
            # print("{}".format(self.client_list[stored_location[1]].data))

            # Transfer Complete, write to file
            if self.client_list[stored_location[1]].number_of_packets == len(self.client_list[stored_location[1]].data):
                print("{}:{} has finished sending all packets".format(client.ip_address, client.port_number))
                f = open(self.client_list[stored_location[1]].filename, "ab")
                for i in range(len(self.client_list[stored_location[1]].data)):
                    f.write(bytes(self.client_list[stored_location[1]].data[i]))
                    # TODO Debug
                    # print("Wrote {} times".format(i))
                f.close()

        else:
            print("{}:{} has connected for the first time".format(client.ip_address, client.port_number))
            # First connection we assume the packet only contains the number of packets with no data :(
            client.number_of_packets = int(message.decode())
            print("{}:{} will send {} packets".format(client.ip_address, client.port_number, client.number_of_packets))
            self.client_list.append(client)
            self.most_recent_client = self.client_list[-1]


if __name__ == "__main__":
    server = UdpFileTransferServer()
    print("Server Running and waiting for connections")
    server.run()
