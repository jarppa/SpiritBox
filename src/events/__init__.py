#!/usr/bin/env python3


class Event:
    def __init__(self, ecls, event, data=None):
        self.ecls = ecls
        self.event = event
        self.data = data

    @property
    def code(self):
        return self.event[0]

    @property
    def name(self):
        return self.event[1]

    @property
    def event_class(self):
        return self.ecls

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
