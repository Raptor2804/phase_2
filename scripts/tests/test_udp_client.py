"""
Requires you to run udp_server.py before running this test because at the moment I'm not dealing with threading
"""


import udp_client


def test_single_client_lower():
    """
    Basic test to check client and server connection
    """
    client_1 = udp_client.UdpClient()

    client_1.send_message("hello world")
    message = client_1.receive_message()
    assert message == "HELLO WORLD"


def test_single_client_mixed():
    """
    These are honestly only here to show my group examples of using pytest. These tests are redundant.
    """
    client_1 = udp_client.UdpClient()

    client_1.send_message("HeLlO wOrld")
    message = client_1.receive_message()
    assert message == "HELLO WORLD"


def test_single_client_upper():
    """
    These are honestly only here to show my group examples of using pytest. These tests are redundant.
    """
    client_1 = udp_client.UdpClient()

    client_1.send_message("HELLO WORLD")
    message = client_1.receive_message()
    assert message == "HELLO WORLD"


def test_three_client_lower():
    """
    This tests the server with three clients and ensures it functions with all three
    """
    client_1 = udp_client.UdpClient()
    client_2 = udp_client.UdpClient()
    client_3 = udp_client.UdpClient()

    client_1.send_message("client 1")
    message_1 = client_1.receive_message()

    client_2.send_message(" client 2")
    message_2 = client_2.receive_message()

    client_3.send_message(" client 3")
    message_3 = client_3.receive_message()

    assert (message_1 + message_2 + message_3) == "CLIENT 1 CLIENT 2 CLIENT 3"


def test_multi_client_lower():
    """
    Test with 1000 separate connections from unique clients
    """
    for i in range(1000):
        msg = "test {}".format(i)
        client = udp_client.UdpClient()
        client.send_message(msg)

