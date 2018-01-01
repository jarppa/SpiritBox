#!/usr/bin/env python3

from plugin_factory import PluginFactory


class EventInterface:
    def __init__(self):
        pass

    def post_event(self, event):
        pass

    def close(self):
        pass


class EventOutFactory(PluginFactory):
    def __init__(self):
        PluginFactory.__init__(self, "event_")
