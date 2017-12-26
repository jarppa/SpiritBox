#!/usr/bin/env python3

from plugin_factory import PluginFactory


class ControllerFactory(PluginFactory):
    def __init__(self):
        PluginFactory.__init__(self, "cntrl_")


class Controller:
    def __init__(self):
        pass

    '''
        Blocking event wait
    '''
    def event(self):
        return None

    '''
        Async event wait
    '''
    def async_event_handler(self, callback):
        pass

