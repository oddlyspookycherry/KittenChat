from argparse import ArgumentParser
from config import *
from utils import ThreadResult, is_valid_ip
import socket
import threading
import time

class PeerConnection():
    def __init__(self, peer_ip : str, my_port : int, peer_port : int, client_name : str) -> None:
        if not is_valid_ip(peer_ip):
            raise ValueError("Peer IP invalid")
        self.peer_ip = peer_ip

        self.port = my_port or DEFAULT_PORT
        self.peer_port = peer_port or DEFAULT_PORT

        if len(client_name) > MAX_NAME_SIZE:
            raise ValueError("Client name too long")
        self.name = client_name
        self.peer_name = None

def init_recv_socket(res: ThreadResult):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as welcome_socket:
        welcome_socket.bind(('', my_port))
        welcome_socket.listen(1)

        while True:
            recv_socket, peer_addr = welcome_socket.accept()

            # if anyone except the peer is connected, close the connection immediatelly
            if peer_addr[0] == peer_ip:
                res.result = recv_socket
                return
            
            recv_socket.close()

def init_send_socket(res: ThreadResult):
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            send_socket.connect((peer_ip, peer_port))
            res.result = send_socket
            return
        except:
            time.sleep(1)
            continue

def sender(sock):
    pass

def receiver(sock):
    pass

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
    


    # Peers connect
    send_socket_res = ThreadResult()
    recv_socket_res = ThreadResult()
    init_send_thread = threading.Thread(target=init_send_socket, args=(send_socket_res,))
    init_recv_thread = threading.Thread(target=init_recv_socket, args=(recv_socket_res,))
    init_send_thread.start()
    init_recv_thread.start()
    init_send_thread.join()
    init_recv_thread.join()
    send_socket = send_socket_res.result
    send_socket: socket.socket
    recv_socket = recv_socket_res.result
    recv_socket: socket.socket
    print("Connection with kitten-peer established!")

    send_thread = threading.Thread(target=sender, args=(send_socket,))
    recv_thread = threading.Thread(target=receiver, args=(recv_socket,))
    send_thread.start()
    recv_thread.start()

    send_thread.join()
    recv_thread.join()

if __name__ == "__main__":
    main()