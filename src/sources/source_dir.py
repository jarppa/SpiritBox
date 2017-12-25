#!/usr/bin/env python3

import os

from sources import TrackSource


def instantiate(from_uri):
    return DirSource(from_uri)


class DirSource(TrackSource):
    def __init__(self, uri):
        TrackSource.__init__(self)
        self.path = uri[5:]  # dir:/
        
        for f in os.listdir(self.path):
            if f.endswith(".mp3"):
                self.tracks.append(os.path.join(self.path, f))
