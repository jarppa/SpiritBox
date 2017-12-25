#!/usr/bin/env python3

from events.control_events import *
from events import Event

from controllers import Controller


def instantiate():
    return ConsoleController()


class ConsoleController(Controller):
    def __init__(self):
        Controller.__init__(self)

    def event(self):
        while 1:
            key = input("-->")
            if key == "quit" or key == "q":
                return Event(CONTROL_EVENT_QUIT)
            elif key == "next":
                return Event(CONTROL_EVENT_NEXT)
            elif key == "prev":
                return Event(CONTROL_EVENT_PREV)
            elif key == "play":
                return Event(CONTROL_EVENT_PLAY)
            elif key == "stop":
                return Event(CONTROL_EVENT_STOP)
            elif key == "pause":
                return Event(CONTROL_EVENT_PAUSE)
            elif key == "volup" or key == "u":
                return Event(CONTROL_EVENT_VOL_UP)
            elif key == "voldown" or key == "d":
                return Event(CONTROL_EVENT_VOL_DOWN)
            elif key == "list":
                return Event(CONTROL_EVENT_LIST)
            elif key.startswith("jump "):
                try:
                    index = int(key[5:])
                except ValueError:
                    print("Invalid index")
                    continue

                return Event(CONTROL_EVENT_JUMP, index)
            elif key == "mute" or key == "m":
                return Event(CONTROL_EVENT_MUTE)
            elif key == "unmute" or key == "n":
                return Event(CONTROL_EVENT_UNMUTE)
            else:
                print("Unknown command")
