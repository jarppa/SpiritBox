#!/usr/bin/env python3

PLAYER_EVENT_STARTED = (1,"Started")
PLAYER_EVENT_STOPPED = (2,"Stopped")
PLAYER_EVENT_PAUSED = (3,"Paused")
PLAYER_EVENT_VOLUME_CHANGED = (4,"Vol. changed")
PLAYER_EVENT_TRACK_CHANGED = (5,"Track changed")
PLAYER_EVENT_TRACK_INFO = (6,"Track info")
PLAYER_EVENT_ERROR = (7,"Error")

class PlayerEvent():
    def __init__(self, player_event):
        self.event = player_event
        
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

class Player():
    
    def __init__(self):
        self.event_cb = None
        self.playlist = None
        
    def set_event_callback(self, event_cb):
        self.event_cb = event_cb
    
    def on_event(self, event):
        if self.event_cb:
            self.event_cb(PlayerEvent(event))
    
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