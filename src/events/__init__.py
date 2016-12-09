#!/usr/bin/env python3


class Event:
    def __init__(self, event, data=None):
        self.event = event
        self.data = data

    @property
    def code(self):
        return self.event[0]

    @property
    def name(self):
        return self.event[1]

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
