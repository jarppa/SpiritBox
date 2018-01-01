#!/usr/bin/env python3

import socket
import sys

from google.protobuf import text_format

sys.path.append("../src/plugins")

from events_pb2 import *

HOST, PORT = "localhost", 7777

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    sock.setblocking(True)

    while 1:
        ser = sock.recv(4096)

        ev = EventMessage()
        ev.ParseFromString(ser)
        print(text_format.MessageToString(ev))

