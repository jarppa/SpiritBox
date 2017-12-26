#!/usr/bin/env python3

import os
import traceback
import importlib

from plugin_factory import PluginFactory

from events.player_events import PlayerEvent
from sources import Playlist

# import threading


class Player:
    
    def __init__(self):
        self.event_cb = None
        self._playlist = Playlist()
        self._playing = False
        self._muted = False

    def set_event_callback(self, event_cb):
        self.event_cb = event_cb
    
    def on_event(self, event, data=None):
        if self.event_cb:
            self.event_cb(PlayerEvent(event, data))

    @property
    def playlist(self):
        return self._playlist

    @playlist.setter
    def playlist(self, playlist):
        self._playlist = playlist

    @playlist.getter
    def playlist(self):
        return self._playlist

    @property
    def muted(self):
        return self._muted

    @muted.getter
    def muted(self):
        return self._muted

    @muted.setter
    def muted(self, m):
        self._muted = m
        if m:
            self.mute()
        else:
            self.unmute()

    @property
    def playing(self):
        return self._playing

    @playing.getter
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, p):
        self._playing = p
        if p:
            self.play()
        else:
            self.pause()

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

    def mute(self):
        pass

    def unmute(self):
        pass

    def get_current_track(self):
        if self.playlist:
            return self.playlist.current_title()
        return None

    def play_track(self, track):
        pass


class PlayerFactory(PluginFactory):
    def __init__(self):
        PluginFactory.__init__(self, "player_")
