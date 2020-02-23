"""
File where all functions associated with the connection (client-server) are defined: create and close connection, and
receive and send messages
"""

from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads

HEADER_SIZE = 10  # Length that indicates the number of characters in the stream


class Connection:
    """
    A class used to represent a connection of current client with the server. A connection object has attributes:

    :param c_socket: a socket object from which the client is connected to the server
    :type c_socket: socket.socket
    :param message: information that the client wants to send or receive from the server. It has a defined structure
    :type message: Modules.Config.Data.Message
    :param stream: flow of bytes that the client actually sends or receives from the serve (message converted to bytes)
    :type stream: bytes
    """

    def __init__(self, c_socket=None, message=None, stream=b''):
        """
        Constructor of the class
        """
        self.c_socket = c_socket
        self.message = message
        self.stream = stream

    def create_connection(self, host, port):
        """
        Establishes a connection with the server

        :param host: IP address of the server which the client wants to connect
        :type host: str
        :param port: port number for the establishment of the server socket
        :type port: int
        """
        self.c_socket = socket(AF_INET, SOCK_STREAM)
        self.c_socket.connect((host, port))

    def create_message(self, data):
        """
        Creates the bytes flow from the message that the client has fulfilled already. Here the stream of bytes is
        created from the message itself, so it can be sent to the server through the network. The stream contains two
        parts: header and data, where header is a number that represents the length of the data (this field is of
        HEADER_SIZE bytes), and data is the actual payload (stream of the message)

        :param data: message that the client wants to send to the server
        :type data: Modules.Config.Data.Message
        """
        self.message = data
        body = dumps(self.message)
        header = '{:<{}}'.format(len(body), HEADER_SIZE)
        self.stream = bytes(header, 'utf-8') + body

    def send_message(self):
        """
        Sends the bytes stream to the server
        """
        self.c_socket.sendall(self.stream)

    def receive_message(self):
        """
        Receives a stream of bytes from the server. First, the function reads the first HEADER_SIZE bytes to know the
        actual length of the payload. With that, the function starts to receive al received streams, until it reaches the
        length. After that, the received stream is reconstructed and converted to a Message object, so the client is
        is capable of reading it
        """
        new_msg = True
        header_ctrl = True
        msg_len = 0
        self.stream = b''
        while new_msg:
            msg = self.c_socket.recv(20)
            if header_ctrl:
                msg_len = int(msg[:HEADER_SIZE].decode('utf-8'))
                print('Server sent stream of length: {}'.format(msg_len))
                header_ctrl = False

            self.stream += msg
            if len(self.stream) - HEADER_SIZE == msg_len:
                print('Full message received')
                new_msg = False
                header_ctrl = True
                self.message = loads(self.stream[HEADER_SIZE:])

    def close_connection(self):
        """
        Closes connection with the server
        """
        self.c_socket.close()
