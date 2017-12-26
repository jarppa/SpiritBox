#!/usr/bin/env python3

import os

from sources import TrackSource


def instantiate(args):
    return DirSource(args)


class DirSource(TrackSource):
    def __init__(self, path):
        TrackSource.__init__(self)
        self.path = path
        
        for f in os.listdir(self.path):
            if f.endswith(".mp3"):
                self.tracks.append(os.path.join(self.path, f))
