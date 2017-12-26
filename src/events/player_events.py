#!/usr/bin/env python3

from events import Event

PLAYER_EVENT_CLASS = "PlayerEvent"

PLAYER_EVENT_STARTED = (1, "Started")
PLAYER_EVENT_STOPPED = (2, "Stopped")
PLAYER_EVENT_PAUSED = (3, "Paused")
PLAYER_EVENT_VOLUME_CHANGED = (4, "Volume Changed")
PLAYER_EVENT_TRACK_CHANGED = (5, "Track Changed")
PLAYER_EVENT_TRACK_INFO = (6, "Track Info")
PLAYER_EVENT_ERROR = (7, "Error")


class PlayerEvent(Event):
    def __init__(self, event, data=None):
        Event.__init__(self, PLAYER_EVENT_CLASS, event, data)
