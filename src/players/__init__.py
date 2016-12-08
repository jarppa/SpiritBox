#!/usr/bin/env python3

from events.player_events import PlayerEvent

#import threading


class Player:
    
    def __init__(self):
        self.event_cb = None
        self.playlist = None

    def set_event_callback(self, event_cb):
        self.event_cb = event_cb
    
    def on_event(self, event, data=None):
        if self.event_cb:
            self.event_cb(PlayerEvent(event, data))
    
    def set_playlist(self, playlist):
        self.playlist = playlist
    
    def destroy(self):
        pass
    
    def play(self):
        pass
    
    def stop(self):
        pass
    
    def pause(self):
        pass
    
    def prev_track(self):
        pass
    
    def next_track(self):
        pass
    
    def volume_up(self):
        pass
    
    def volume_down(self):
        pass
    
    def set_volume(self, volume):
        pass

    def get_current_track(self):
        if self.playlist:
            return self.playlist.current()
        return None
