from argparse import ArgumentParser
from config import *
from utils import ThreadResult
import socket
import threading
import time

# parsing input arguments
arg_parser = ArgumentParser(prog='kittenchat')
arg_parser.add_argument('-peer_ip', type=str, required=True)
arg_parser.add_argument('-my_port', type=int, required=False)
arg_parser.add_argument('-peer_port', type=int, required=False)
arg_parser.add_argument('-name', type=str, required=True)
args = arg_parser.parse_args()
peer_ip, my_port, peer_port, client_name = \
    args.peer_ip, args.my_port, args.peer_port, args.name

my_port = my_port or DEFAULT_PORT
peer_port = peer_port or DEFAULT_PORT

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

def main():
    
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
    recv_socket = recv_socket_res.result
    print("Connection with kitten-peer established!")

if __name__ == "__main__":
    main()