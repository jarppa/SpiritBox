#!/usr/bin/env python3

from events.control_events import *

from controllers import Controller


def instantiate(args):
    return ConsoleController()


class ConsoleController(Controller):
    def __init__(self):
        Controller.__init__(self)

    def print_commands(self):
        print("quit | q\nnext\nprev\nplay\nstop\npause\nvolup | u\nvoldown | d\nlist\njump\nmute | m\nunmute | n\nhelp | ?\n")

    def event(self):
        while 1:
            key = input("-->")
            if key == "quit" or key == "q":
                return ControlEvent(CONTROL_EVENT_QUIT)
            elif key == "next":
                return ControlEvent(CONTROL_EVENT_NEXT)
            elif key == "prev":
                return ControlEvent(CONTROL_EVENT_PREV)
            elif key == "play":
                return ControlEvent(CONTROL_EVENT_PLAY)
            elif key == "stop":
                return ControlEvent(CONTROL_EVENT_STOP)
            elif key == "pause":
                return ControlEvent(CONTROL_EVENT_PAUSE)
            elif key == "volup" or key == "u":
                return ControlEvent(CONTROL_EVENT_VOL_UP)
            elif key == "voldown" or key == "d":
                return ControlEvent(CONTROL_EVENT_VOL_DOWN)
            elif key == "list":
                return ControlEvent(CONTROL_EVENT_LIST)
            elif key.startswith("jump "):
                try:
                    index = int(key[5:])
                except ValueError:
                    print("Invalid index")
                    continue

                return ControlEvent(CONTROL_EVENT_JUMP, index)
            elif key == "mute" or key == "m":
                return ControlEvent(CONTROL_EVENT_MUTE)
            elif key == "unmute" or key == "n":
                return ControlEvent(CONTROL_EVENT_UNMUTE)
            elif key == "?" or key == "help":
                self.print_commands()
                continue
            else:
                print("Unknown command. Try \"help\"")
