from argparse import ArgumentParser
from config import *
from utils import ThreadResult, is_valid_ip
import socket
import threading
import time

class PeerParticipant():
    def __init__(self, my_port: int, name: str) -> None:
        self.port = my_port or DEFAULT_PORT

        if len(name) > MAX_NAME_SIZE:
            raise ValueError("Client name too long")
        self.name = name

    def initialize_connection(self, peer_ip: str, peer_port: int) -> None:
        if not is_valid_ip(peer_ip):
            raise ValueError("Peer IP invalid")
        self.peer_ip = peer_ip
        self.peer_port = peer_port or DEFAULT_PORT
        self.peer_addr = (self.peer_ip, self.peer_port)
        self.peer_name = None

        # Peers connect
        send_socket_res = ThreadResult()
        recv_socket_res = ThreadResult()
        init_send_thread = threading.Thread(target=self._init_send_socket, args=(send_socket_res,))
        init_recv_thread = threading.Thread(target=self._init_recv_socket, args=(recv_socket_res,))
        init_send_thread.start()
        init_recv_thread.start()
        init_send_thread.join()
        init_recv_thread.join()
        self.send_socket = send_socket_res.result
        self.send_socket: socket.socket
        self.recv_socket = recv_socket_res.result
        self.recv_socket: socket.socket

    def send_message(self, msg: str) -> None:
        msg_data_bin = msg.encode()
        msg_len = len(msg_data_bin)
        msg_len_bin = msg_len.to_bytes(MESSAGE_LEN_BYTES)
        data_to_send = msg_len_bin + msg_data_bin
        self.send_socket.sendall(data_to_send)

    def recv_message(self) -> str:
        length_bytes = self.recv_socket.recv(MESSAGE_LEN_BYTES)
        
        if not length_bytes:
            return None # Connection closed
        message_length = int.from_bytes(length_bytes)        

        message_content_bin = b''
        while len(message_content_bin) < message_length:
            chunk = self.recv_socket.recv(min(BUFF_SIZE, message_length - len(message_content_bin)))
            if not chunk:
                return None  # Connection closed
            message_content_bin += chunk
        message_content = message_content_bin.decode()
        return message_content

    def _init_recv_socket(self, res: ThreadResult):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as welcome_socket:
            welcome_socket.bind(('', self.port))
            welcome_socket.listen(1)

            while True:
                recv_socket, peer_addr = welcome_socket.accept()

                # if anyone except the peer is connected, close the connection immediatelly
                if peer_addr[0] == self.peer_ip:
                    res.result = recv_socket
                    return
                
                recv_socket.close()

    def _init_send_socket(self, res: ThreadResult):
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                send_socket.connect(self.peer_addr)
                res.result = send_socket
                return
            except:
                time.sleep(1)
                continue


def sender(peer_participant: PeerParticipant):
    while True:
        msg = input()
        peer_participant.send_message(msg)

def receiver(peer_participant: PeerParticipant):
    while True:
        peer_msg = peer_participant.recv_message()
        print(peer_msg)

def main():
    
    # parsing input arguments
    arg_parser = ArgumentParser(prog='kittenchat')
    arg_parser.add_argument('-peer_ip', type=str, required=True)
    arg_parser.add_argument('-my_port', type=int, required=False)
    arg_parser.add_argument('-peer_port', type=int, required=False)
    arg_parser.add_argument('-name', type=str, required=True)
    args = arg_parser.parse_args()
    peer_ip, my_port, peer_port, client_name = \
        args.peer_ip, args.my_port, args.peer_port, args.name
    
    this_participant = PeerParticipant(my_port, client_name)
    this_participant.initialize_connection(peer_ip, peer_port)
    print("Connection with kitten-peer established!")

    send_thread = threading.Thread(target=sender, args=(this_participant,))
    recv_thread = threading.Thread(target=receiver, args=(this_participant,))
    send_thread.start()
    recv_thread.start()
    send_thread.join()
    recv_thread.join()

if __name__ == "__main__":
    main()