#!/usr/bin/env python3

from events.control_events import *
from events.player_events import *
from events.app_events import *

from interfaces import EventInterface


def instantiate(args):
    return ConsoleEventInterface()


class ConsoleEventInterface(EventInterface):
    def __init__(self):
        EventInterface.__init__(self)

    def post_event(self, event):
        if event.event_class == PLAYER_EVENT_CLASS:
            print("Player event: %s" % event)
        elif event.event_class == CONTROL_EVENT_CLASS:
            print("Control event: %s" % event)
        elif event.event_class == APP_EVENT_CLASS:
            if event == APP_EVENT_INDICATION:
                print("App indication: %s" % event.data.data)
            else:
                print("App event: %s" % event)
