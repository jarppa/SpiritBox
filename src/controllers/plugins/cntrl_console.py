#!/usr/bin/env python3

from events.control_events import *

from controllers import Controller


def instantiate():
    return ConsoleController()


class ConsoleController(Controller):
    def __init__(self):
        Controller.__init__(self)
        
    def get_event(self):
        key = None
        while 1:
            key = input("-->")
            if key == "quit" or key=="q":
                return CONTROL_EVENT_QUIT
            elif key == "next":
                return CONTROL_EVENT_NEXT
            elif key == "prev":
                return CONTROL_EVENT_PREV
            elif key == "play":
                return CONTROL_EVENT_PLAY
            elif key == "stop":
                return CONTROL_EVENT_STOP
            elif key == "pause":
                return CONTROL_EVENT_PAUSE
            elif key == "volup" or key == "u":
                return CONTROL_EVENT_VOL_UP
            elif key == "voldown" or key == "d":
                return CONTROL_EVENT_VOL_DOWN
            else:
                print ("Unknown command")
    
