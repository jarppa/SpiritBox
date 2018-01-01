#!/usr/bin/env python3

import sys
import socketserver
import threading
import queue

from events.control_events import *
from events.player_events import *
from events.app_events import *

sys.path.append(".")

from events_pb2 import EventMessage, AppEvent, GenericEvent
from google.protobuf import message

from interfaces import EventInterface

events = queue.Queue()


def instantiate(args):
    return ProtobufEventInterface(args)


class MyServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, request_handler_class):
        super().__init__(server_address, request_handler_class, True)
        self.clients = set()
        self.clients_lock = threading.Lock()

    def add_client(self, client):
        with self.clients_lock:
            self.clients.add(client)

    def send(self, data):
        with self.clients_lock:
            for c in tuple(self.clients):
                c.write(data)

    def remove_client(self, client):
        with self.clients_lock:
            try:
                self.clients.remove(client)
            except:
                pass

    def shutdown(self):
        super().shutdown()

        with self.clients_lock:
            for c in self.clients:
                c.stop()


class MyHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def setup(self):
        super().setup()
        self.server.add_client(self)

    def handle(self):
        """ Will not handle any requests from clients """
        print("New client")
        while 1:
            try:
                d = self.request.recv(1024)
            except:
                print("Read failed")
                self.server.remove_client(self)
                break
        # pass

    def finish(self):
        print("Client left")
        self.server.remove_client(self)
        super().finish()

    def write(self, data):
        try:
            self.request.send(data)
        except:
            print("Write failed")
            self.server.remove_client(self)

    def stop(self):
        self.request.close()


class ServerRunner(threading.Thread):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        self.server.serve_forever()
        print("Server closed")

    def stop(self):
        self.server.shutdown()


class ProtobufEventInterface(EventInterface):
    def __init__(self, args):
        super().__init__()
        try:
            port = int(args)
        except ValueError:
            port = 7777

        self.server = MyServer(("0.0.0.0", port), MyHandler)
        self.server_runner = ServerRunner(self.server)
        self.server_runner.start()

    def close(self):
        self.server_runner.stop()

    def post_event(self, event):
        ev = EventMessage()
        if event.event_class == APP_EVENT_CLASS:
            """ App events """
            ev.type = EventMessage.APP_EVENT
            if event == APP_EVENT_INDICATION:
                ev.app_event.type = AppEvent.INDICATION
                if event.data.type == APP_INDICATION_PLAYLIST:
                    ev.app_event.indication.type = AppEvent.AppIndication.APP_INDICATION_PLAYLIST
                    for t in event.data.data:
                        title = ev.app_event.indication.playlist.titles.add()
                        title.name = t
                else:
                    pass
            else:
                ev.app_event.type = AppEvent.GENERIC
                ev.app_event.generic.code = event.code
                if event.data:
                    ev.app_event.generic.data = str(event.data)

        elif event.event_class == CONTROL_EVENT_CLASS:
            ev.type = EventMessage.CONTROL_EVENT
            ev.control_event.code = event.code
            if event.data:
                ev.control_event.data = str(event.data)

        elif event.event_class == PLAYER_EVENT_CLASS:
            ev.type = EventMessage.PLAYER_EVENT
            ev.player_event.code = event.code
            if event.data:
                ev.player_event.data = str(event.data)

        else:
            pass

        self.server.send(ev.SerializeToString())
