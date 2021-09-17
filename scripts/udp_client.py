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

    def send_message(self, message):
        """
        send message to designated server_address

        :param message: Data to be sent to the server
        :return: # of bytes sent
        """
        self.client_socket.sendto(message.encode(), (self.server_name, self.server_port))

    def receive_message(self):
        """
        receive a message from socket using pre-allocated buffer

        :return: returns (message, server_address)
        """
        message = self.client_socket.recvfrom(2048)
        return message[0].decode()


if __name__ == "__main__":
    client = UdpClient()
    client.send_message("Testing")
    print(client.receive_message())
