from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads

HEADER_SIZE = 10  # Length that indicates the number of characters in the stream


class Connection():


    def __init__(self, c_socket='', message='', stream=b''):
        self.c_socket = c_socket
        self.message = message
        self.stream = stream

    def create_connection(self, host, port):
        self.c_socket = socket(AF_INET, SOCK_STREAM)
        self.c_socket.connect((host, port))

    def create_message(self, data):
        self.message = data
        body = dumps(self.message)
        header = '{:<{}}'.format(len(body), HEADER_SIZE)
        self.stream = bytes(header, 'utf-8') + body

    def send_message(self):
        self.c_socket.sendall(self.stream)

    def receive_message(self):
        new_msg = True
        header_ctrl = True
        self.stream = b''
        while new_msg:
            msg = self.c_socket.recv(20)
            if header_ctrl:
                msg_len = int(msg[:HEADER_SIZE].decode('utf-8'))
                print('The length of the stream is: {}'.format(str(msg_len)))
                header_ctrl = False

            self.stream += msg
            if len(self.stream) - HEADER_SIZE == msg_len:
                print('Full message received')
                new_msg = False
                header_ctrl = True
                self.message = loads(self.stream[HEADER_SIZE:])

    def close_connection(self):
        self.c_socket.close()