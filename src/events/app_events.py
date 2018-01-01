#!/usr/bin/env python3

from events import Event

APP_EVENT_CLASS = "AppEvent"

APP_EVENT_INIT = (1, "Init")
APP_EVENT_READY = (2, "Ready")
APP_EVENT_SHUTDOWN = (3, "Shutdown")
APP_EVENT_ERROR = (4, "Error")
APP_EVENT_INDICATION = (5, "Indication")

APP_INDICATION_PLAYLIST = (1, "Playlist")


class AppIndication:
    def __init__(self, indication_type, data=None):
        self.ind_type = indication_type
        self.ind_data = data

    @property
    def data(self):
        return self.ind_data

    @property
    def type(self):
        return self.ind_type


class AppEvent(Event):
    def __init__(self, event, data=None):
        Event.__init__(self, APP_EVENT_CLASS, event, data)
