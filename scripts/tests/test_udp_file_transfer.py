#!/usr/bin/env python3

import subprocess
import udp_client

"""
Runs all the test relevant to phase 2. test_udp_file_transfer.py must be opened in a separate terminal
"""


def test_multi_client_multi_messages():
    client_1 = udp_client.UdpClient()
    client_2 = udp_client.UdpClient()
    client_3 = udp_client.UdpClient()

    client_1.send_message(str(10))
    client_2.send_message(str(5))
    client_3.send_message(str(1))

    for i in range(10):
        client_1.send_message("Test")
        if i % 2 == 0:
            client_2.send_message("Test")
    client_3.send_message("Test")
