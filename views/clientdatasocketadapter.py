import socket
import pickle

HEADERSIZE = 10

class clientDataSocketAdapter:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", 32000))

    def __del__(self):
        self.sock.close()

    def get_view_data(self):
        return(pickle.loads(self.__receive_message()[HEADERSIZE:]))

    def __receive_message(self):
        chunk = self.sock.recv(16)
        message_length = int(chunk[:HEADERSIZE])
        message = chunk
        while True:
            chunk = self.sock.recv(16)
            message += chunk
            if (len(message) - HEADERSIZE) == message_length:
                return(message)
