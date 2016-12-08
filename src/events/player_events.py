#!/usr/bin/env python3

PLAYER_EVENT_STARTED = (1, "Started")
PLAYER_EVENT_STOPPED = (2, "Stopped")
PLAYER_EVENT_PAUSED = (3, "Paused")
PLAYER_EVENT_VOLUME_CHANGED = (4, "Volume Changed")
PLAYER_EVENT_TRACK_CHANGED = (5, "Track Changed")
PLAYER_EVENT_TRACK_INFO = (6, "Track Info")
PLAYER_EVENT_ERROR = (7, "Error")


class PlayerEvent:
    def __init__(self, player_event, data=None):
        self.event = player_event
        self.data = data

    def __str__(self):
        return self.event[1]

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        elif isinstance(other, int):
            return self.event[0] == other

        elif isinstance(other, tuple):
            return self.event[0] == other[0]

        return False

    def __ne__(self, other):
        return not self.__eq__(other)
