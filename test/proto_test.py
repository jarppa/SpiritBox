#!/usr/bin/env python3

import socket
import sys

sys.path.append("../src/plugins")

from control_pb2 import *

HOST, PORT = "localhost", 6666
event = sys.argv[1]
if len(sys.argv) > 2:
    data = sys.argv[2]
else:
    data = ""

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    msg = ControlMessage()
    msg.event = int(event)
    msg.data = data
    sock.sendall(msg.SerializeToString())
