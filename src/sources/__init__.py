#!/usr/bin/env python3

import os
import traceback
import importlib
import sys

sys.path.append(os.path.dirname(__file__))

class Playlist():
    def __init__(self, source):
        self.position = -1
        self.source = source

    def reset(self):
        self.position = -1
        
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
    
    def current(self):
        if self.position >= 0:
            return self.source.at(self.position)

        return None

    
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
            if f.startswith("handler_") and f.endswith(".py"):
                try:
                    cls = importlib.import_module(f[:-3],"sources")
                    self.uri_handlers[f[8:-3]] = cls
                    
                except:
                    print ("Cannot import module")
                    traceback.print_exc()
                    
    
    def get_available_types(self):
        return self.uri_handlers.keys()
    
    
class TrackSource():
    def __init__(self, uri):
        self.uri = uri
        self.sources = []
        
    def at(self, index):
        if index < 0 or index >= len(self.sources):
            return None
        else:
            return self.sources[index]
    
    def all_items(self):
        return self.sources
    
    def size(self):
        return len(self.all_items())
    