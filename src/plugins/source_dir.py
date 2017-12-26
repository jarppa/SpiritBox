#!/usr/bin/env python3

import os

from sources import TrackSource


def instantiate(args):
    return DirSource(args)
    return Playlist(self.uri_handlers[from_uri.split(':')[0]].instantiate(from_uri))

class DirSource(TrackSource):
    def __init__(self, path):
        TrackSource.__init__(self)
        self.path = path
        
        for f in os.listdir(self.path):
            if f.endswith(".mp3"):
                self.tracks.append(os.path.join(self.path, f))
