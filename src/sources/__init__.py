#!/usr/bin/env python3

from plugin_factory import PluginFactory


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

    def contains_title(self, title):
        return title in self.tracks


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
            if self.source.contains_title(t):
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
    

class SourceFactory(PluginFactory):
    
    def __init__(self):
        PluginFactory.__init__(self, "source_")
