#!/usr/bin/env python3

from events import Event

CONTROL_EVENT_CLASS = "ControlEvent"

CONTROL_EVENT_PLAY = (1, "play")
CONTROL_EVENT_STOP = (2, "stop")
CONTROL_EVENT_PAUSE = (3, "pause")
CONTROL_EVENT_NEXT = (4, "next")
CONTROL_EVENT_PREV = (5, "prev")
CONTROL_EVENT_VOL_UP = (6, "vol_up")
CONTROL_EVENT_VOL_DOWN = (7, "vol_down")
CONTROL_EVENT_QUIT = (8, "quit")
CONTROL_EVENT_LIST = (9, "list")
CONTROL_EVENT_JUMP = (10, "jump")
CONTROL_EVENT_MUTE = (11, "mute")
CONTROL_EVENT_UNMUTE = (12, "unmute")
CONTROL_EVENT_PLAYPAUSE = (13, "playpause")
CONTROL_EVENT_MUTEUNMUTE = (14, "muteunmute")

__control_events = (CONTROL_EVENT_PLAY,
                    CONTROL_EVENT_STOP,
                    CONTROL_EVENT_PAUSE,
                    CONTROL_EVENT_NEXT,
                    CONTROL_EVENT_PREV,
                    CONTROL_EVENT_VOL_UP,
                    CONTROL_EVENT_VOL_DOWN,
                    CONTROL_EVENT_QUIT,
                    CONTROL_EVENT_LIST,
                    CONTROL_EVENT_JUMP,
                    CONTROL_EVENT_MUTE,
                    CONTROL_EVENT_UNMUTE,
                    CONTROL_EVENT_PLAYPAUSE,
                    CONTROL_EVENT_MUTEUNMUTE)

control_event_id_map = dict((i+1, v) for i, v in enumerate(__control_events))


class ControlEvent(Event):
    def __init__(self, event, data=None):
        Event.__init__(self, CONTROL_EVENT_CLASS, event, data)
