#!/usr/bin/env python3

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
            if key == "quit":
                return "EVENT_QUIT"
            elif key == "next":
                return "EVENT_NEXT"
            elif key == "prev":
                return "EVENT_PREV"
            elif key == "play":
                return "EVENT_PLAY"
            elif key == "stop":
                return "EVENT_STOP"
            elif key == "pause":
                return "EVENT_PAUSE"
            elif key == "volup":
                return "EVENT_VOL_UP"
            elif key == "voldown":
                return "EVENT_VOL_DOWN"
            else:
                print ("Unknown command")
    
