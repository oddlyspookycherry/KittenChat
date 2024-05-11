from argparse import ArgumentParser
from config import *
import socket

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
