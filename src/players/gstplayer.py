#!/usr/bin/env python3

import threading

from players import Player, \
                    PLAYER_EVENT_STARTED, \
                    PLAYER_EVENT_STOPPED, \
                    PLAYER_EVENT_PAUSED, \
                    PLAYER_EVENT_ERROR,\
                    PLAYER_EVENT_TRACK_CHANGED,\
                    PLAYER_EVENT_VOLUME_CHANGED

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import os

Gst.init(None)
mainloop = GObject.MainLoop()

class GstThread(threading.Thread):
    def __init__(self, mainloop):
        threading.Thread.__init__(self)
        self.mainloop = mainloop
        
    def run(self):
        self.mainloop.run()
        print ("GST mainloop finished")


class GstPlayer(Player):
    def __init__(self, output=None):
        Player.__init__(self)
        
        self.volume = 0.5
        
        self.pipeline = Gst.Pipeline()
        
        self.source = Gst.ElementFactory.make("filesrc", "source")
        self.decoder = Gst.ElementFactory.make("mad", "decoder")
        self.convert = Gst.ElementFactory.make('audioconvert', 'convert')
        self.volctrl = Gst.ElementFactory.make('volume', "volume")
        self.output = Gst.ElementFactory.make("autoaudiosink", "sink")

        if self.source and self.decoder and self.convert and self.output and self.volctrl:
            self.pipeline.add(self.source)
            self.pipeline.add(self.decoder)
            self.pipeline.add(self.convert)
            self.pipeline.add(self.volctrl)
            self.pipeline.add(self.output)
            
            self.source.link(self.decoder)
            self.decoder.link(self.convert)
            self.convert.link(self.volctrl)
            self.volctrl.link(self.output)
        
            bus = self.pipeline.get_bus()
            bus.add_signal_watch()
            bus.connect("message", self._on_bus_message)
        
            self.volctrl.set_property('volume', self.volume)
        
            self.pipeline.set_state(Gst.State.READY)
        
            self.mainloop_thread = GstThread(mainloop)
        
            self.mainloop_thread.start()

        
    def _on_bus_message(self, bus, message):
        t = message.type

        if t == Gst.MessageType.EOS:
            self.next_track()
        elif t == Gst.MessageType.ERROR:
            print (str(message.parse_error()))
            self.pipeline.set_state(Gst.State.NULL)
            self.on_event(PLAYER_EVENT_ERROR)
        
        elif t == Gst.MessageType.STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            self.state = new
            #print("State changed from {0} to {1}".format(
            #    Gst.Element.state_get_name(old), Gst.Element.state_get_name(new)))

            if message.src != self.output:
                return
            
            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                self.on_event(PLAYER_EVENT_STARTED)
            elif old == Gst.State.READY and new == Gst.State.PLAYING:
                self.on_event(PLAYER_EVENT_STARTED)
            elif old == Gst.State.PLAYING and new == Gst.State.PAUSED:
                self.on_event(PLAYER_EVENT_PAUSED)
            elif old == Gst.State.READY and new == Gst.State.PAUSED:
                self.on_event(PLAYER_EVENT_PAUSED)
            elif new == Gst.State.NULL:
                self.on_event(PLAYER_EVENT_STOPPED)
         

    def destroy(self):
        self.pipeline.set_state(Gst.State.NULL)
        mainloop.quit()
        self.mainloop_thread.join()


    def play(self):
        Player.play(self)
        self.pipeline.set_state(Gst.State.PLAYING)
    
    
    def stop(self):
        Player.stop(self)
        self.pipeline.set_state(Gst.State.READY)
    
    
    def pause(self):
        Player.pause(self)
        self.pipeline.set_state(Gst.State.PAUSED)
    
    
    def prev_track(self):

        t = self.playlist.prev()
        if t:
            self.stop()
            self._play_track(t)
        
    
    def next_track(self):

        t = self.playlist.next()
        if t:
            self.stop()
            self._play_track(t)
        
    
    def volume_up(self):
        self.volume += 0.1
        
        if self.volume > 1.0:
            self.volume = 1.0
            
        self._set_volume()
    
    
    def volume_down(self):
        self.volume -= 0.1
        
        if self.volume < 0.0:
            self.volume = 0.0
            
        self._set_volume()
    
    
    def set_volume(self, volume):
        if isinstance(volume, float):
            if volume > 1.0:
                self.volume = 1.0
            elif volume < 0.0:
                self.volume = 0.0
        
        elif isinstance(volume, int):
            if volume > 100:
                self.volume = 1.0
            elif volume < 0:
                self.volume = 0.0
        else:
            raise ValueError
        
        self._set_volume()
        
        
    def get_current_track(self):
        return self.playlist.current()
    
    def _play_track(self, track):
        print ("Play: "+ track)
        self.pipeline.set_state(Gst.State.READY)
        self.source.set_property('location',track)
        self.pipeline.set_state(Gst.State.PLAYING)
        #self.on_event(PLAYER_EVENT_TRACK_CHANGED)
        
    def _set_volume(self):
        self.volctrl.set_property('volume', self.volume)
        self.on_event(PLAYER_EVENT_VOLUME_CHANGED)
    