#!/usr/bin/env python3

import sys

from events.control_events import *

from controllers import Controller


def instantiate(args):
    return ProtobufController()


class ProtobufController(Controller):
    def __init__(self):
        Controller.__init__(self)

    def event(self):
        pass
