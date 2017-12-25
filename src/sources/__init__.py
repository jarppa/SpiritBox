#!/usr/bin/env python3

import os
import traceback
import importlib
import sys

sys.path.append(os.path.dirname(__file__))


class TrackSource:
    def __init__(self):
        self.tracks = []

    def at(self, index):
        if index < 0 or index >= len(self.tracks):
            return None
        else:
            return self.tracks[index]

    def all_items(self):
        return self.tracks

    def size(self):
        return len(self.all_items())

    def contains(self, item):
        return item in self.tracks


class Playlist:
    def __init__(self, source=TrackSource()):
        self.position = -1
        self.source = source

    def reset(self):
        self.position = -1

    def track(self, t):
        if isinstance(t, int) and 0 <= t < self.source.size():
            self.position = t
            return self.source.at(t)
        elif isinstance(t, str):
            if self.source.contains(t):
                self.position = self.source.index(t)
                return t

        return None

    def next(self):
        if self.position < self.source.size()-1:
            self.position += 1
            return self.source.at(self.position)
        else:
            return None

    def prev(self):
        if self.position > 0:
            self.position -= 1
            return self.source.at(self.position)
        else:
            return None
    
    def current_title(self):
        if self.position >= 0:
            return self.source.at(self.position)

        return None

    def current_index(self):
        return self.position

    def list_titles(self):
        return self.source.all_items()

    def __str__(self):
        return str(self.source.all_items())
    

class PlaylistFactory:
    
    def __init__(self):
        self.uri_handlers = {}
        self._load_modules()
        
    def create(self, from_uri):
        return Playlist(self.uri_handlers[from_uri.split(':')[0]].instantiate(from_uri))
    
    def _load_modules(self):
        for f in os.listdir(os.path.dirname(__file__)):
            if f.startswith("source_") and f.endswith(".py"):
                try:
                    cls = importlib.import_module(f[:-3], "sources")
                    self.uri_handlers[f[7:-3]] = cls
                    
                except:
                    print("Cannot import module")
                    traceback.print_exc()

    def get_available_types(self):
        return self.uri_handlers.keys()
