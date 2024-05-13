import socket
import time
from argparse import ArgumentParser

HOST = '0.0.0.0'

def main():
    arg_parser = ArgumentParser(prog='networktest')
    arg_parser.add_argument('-peer_ip', type=str, required=True)
    arg_parser.add_argument('-port', type=int, required=True)
    arg_parser.add_argument('--owner', action='store_true', required=False)
    args = arg_parser.parse_args()
    owner, peer_ip, port = args.owner, args.peer_ip, args.port

    if owner:
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        send_socket.bind((HOST, port))
        while True:
            try:
                send_socket.connect((peer_ip, port))
                break
            except:
                time.sleep(1)
                continue
        send_socket.send("hello!".encode())
    else:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        recv_socket.bind((HOST, port))
        try:
            ping_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ping_socket.settimeout(3)
            ping_socket.connect((peer_ip, port))
        except:
            print("Firewall pinged.")
        finally:
            ping_socket.close()
        recv_socket.listen(1)
        owner_socket, owner_address = recv_socket.accept()
        msg = owner_socket.recv(1024).decode()
        print(msg)

if __name__ == "__main__":
    main()