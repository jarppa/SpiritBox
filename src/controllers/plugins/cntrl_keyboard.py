#!/usr/bin/env python3

import sys

from events.control_events import *
from events import Event

from controllers import Controller

sys.path.append(".")

from inputs import get_key, KEYS_AND_BUTTONS, EVENT_TYPES

PRESSED = 1
RELEASED = 0


def instantiate():
    return KeyboardController()


class KeyboardController(Controller):
    def __init__(self):
        Controller.__init__(self)
        self.keys = dict((k, v) for k, v in KEYS_AND_BUTTONS)
        self.types = dict((k, v) for k, v in EVENT_TYPES)
        self.pressed = []

    def get_event(self):
        key = None
        while 1:
            keys = get_key()
            for key in keys:
                if key.ev_type == "Key":
                    if key.state == PRESSED and key.code not in self.pressed:
                        self.pressed.append(key.code)
                    elif key.state == RELEASED:
                        if key.code in self.pressed:
                            self.pressed.remove(key.code)
                            return self.__handle_key(key.code)

    def __handle_key(self, code):
        if code == "KEY_ESC":
            return Event(CONTROL_EVENT_QUIT)
        elif code == "KEY_NEXTSONG":
            return Event(CONTROL_EVENT_NEXT)
        elif code == "KEY_PREVIOUSSONG":
            return Event(CONTROL_EVENT_PREV)
        elif code == "KEY_PLAYPAUSE":
            return Event(CONTROL_EVENT_PLAYPAUSE)
        elif code == "KEY_STOP":
            return Event(CONTROL_EVENT_STOP)
        elif code == "KEY_VOLUMEUP":
            return Event(CONTROL_EVENT_VOL_UP)
        elif code == "KEY_VOLUMEDOWN":
            return Event(CONTROL_EVENT_VOL_DOWN)
        elif code == "KEY_MUTE":
            return Event(CONTROL_EVENT_MUTEUNMUTE)
        else:
            print ("Unknown command")

