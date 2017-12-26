#!/usr/bin/env python3

import sys
import socketserver
import threading

from events.control_events import *

sys.path.append(".")

from control_pb2 import *
from google.protobuf import message

from controllers import Controller

control_messages = []
message_condition = threading.Condition()


def instantiate(args):
    return ProtobufController(args)


class Server(threading.Thread):
    def __init__(self, addr, port):
        threading.Thread.__init__(self)
        self.server = socketserver.TCPServer((addr, port), ControlRequestHandler)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()


class ControlRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        msg = ControlMessage()

        data = self.request.recv(4096)
        try:
            msg.ParseFromString(data)
        except message.EncodeError:
            return

        with message_condition:
            control_messages.append(msg)
            message_condition.notify_all()


class ProtobufController(Controller):
    def __init__(self, args):
        Controller.__init__(self)
        try:
            port = int(args)
        except ValueError:
            port = 6666

        self.server = Server("0.0.0.0", port)
        self.server.start()

    def close(self):
        self.server.stop()

    def event(self):
        with message_condition:
            while not len(control_messages):
                message_condition.wait()

            msg = control_messages.pop(0)
            return ControlEvent(control_event_id_map[msg.event], msg.data)
