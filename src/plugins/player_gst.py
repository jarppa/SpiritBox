#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

import threading

from events.player_events import \
                    PLAYER_EVENT_STARTED, \
                    PLAYER_EVENT_STOPPED, \
                    PLAYER_EVENT_PAUSED, \
                    PLAYER_EVENT_ERROR,\
                    PLAYER_EVENT_TRACK_CHANGED,\
                    PLAYER_EVENT_VOLUME_CHANGED

from players import Player


Gst.init(None)
mainloop = GObject.MainLoop()


def instantiate(args):
    return GstPlayer()


class GstThread(threading.Thread):
    def __init__(self, mainlop):
        threading.Thread.__init__(self)
        self.mainloop = mainlop
        
    def run(self):
        self.mainloop.run()
        # print("GST mainloop finished")


class GstPlayer(Player):
    def __init__(self):
        Player.__init__(self)
        
        self.volume = 50
        
        self.pipeline = Gst.Pipeline()
        
        self.source = Gst.ElementFactory.make("filesrc", "source")
        self.decoder = Gst.ElementFactory.make("decodebin", "decoder")
        self.convert = Gst.ElementFactory.make('audioconvert', 'convert')
        self.volctrl = Gst.ElementFactory.make('volume', "volume")
        self.output = Gst.ElementFactory.make("autoaudiosink", "sink")

        if not self.source:
            # print("Cannot initialize audio source")
            return
        if not self.decoder:
            # print("Cannot initialize audio decoder")
            return
        if not self.convert:
            # print("Cannot initialize audio convert")
            return
        if not self.output:
            # print("Cannot initialize audio output")
            return
        if not self.volctrl:
            # print("Cannot initialize audio volume control")
            return

        self.pipeline.add(self.source)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.convert)
        self.pipeline.add(self.volctrl)
        self.pipeline.add(self.output)
            
        self.source.link(self.decoder)
        self.decoder.link(self.convert)
        self.convert.link(self.volctrl)
        self.volctrl.link(self.output)

        self.decoder.connect("pad-added", self._new_decoded_pad_cb)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._on_bus_message)
        
        self.volctrl.set_property('volume', self.volume/100.0)
        
        self.pipeline.set_state(Gst.State.READY)
        
        self.mainloop_thread = GstThread(mainloop)
        
        self.mainloop_thread.start()

    def _new_decoded_pad_cb(self, dbin, pad):

        if "audio" not in pad.get_current_caps().to_string():
            return
        pad.link(self.convert.get_static_pad("sink"))

    def _on_bus_message(self, bus, message):
        t = message.type

        if t == Gst.MessageType.EOS:
            self.next_track()

        elif t == Gst.MessageType.ERROR:
            print(str(message.parse_error()))
            self.pipeline.set_state(Gst.State.NULL)
            self.on_event(PLAYER_EVENT_ERROR, message.parse_error())
        
        elif t == Gst.MessageType.STATE_CHANGED:
            old, new, pending = message.parse_state_changed()

            if message.src != self.output:
                return
            
            if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
                self.on_event(PLAYER_EVENT_STARTED)
                self.on_event(PLAYER_EVENT_TRACK_CHANGED, self.get_current_track())
            elif old == Gst.State.READY and new == Gst.State.PLAYING:
                self.on_event(PLAYER_EVENT_TRACK_CHANGED, self.get_current_track())
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
        if self.playlist.current_index() == -1:
            t = self.playlist.next()
            if t:
                self._play_track(t)
        else:
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

    def play_track(self, track):
        t = self.playlist.track(track)
        if t:
            self._play_track(t)
        # else:
        #    print("Invalid track: %s" % track)

    def volume_up(self):
        self.volume += 10
        
        if self.volume >= 100:
            self.volume = 100
            
        self._set_volume(self.volume)

    def volume_down(self):
        self.volume -= 10
        
        if self.volume <= 0:
            self.volume = 0
            
        self._set_volume(self.volume)

    def set_volume(self, volume):
        if isinstance(volume, float):
            if volume >= 100:
                self.volume = 100
            elif volume <= 0:
                self.volume = 0
            else:
                self.volume = volume
        
        elif isinstance(volume, int):
            if volume >= 100:
                self.volume = 100
            elif volume <= 0:
                self.volume = 0
            else:
                self.volume = volume

        else:
            raise ValueError
        
        self._set_volume(self.volume)

    def mute(self):
        self._set_volume(0)

    def unmute(self):
        self._set_volume(self.volume)

    def get_current_track(self):
        return self.playlist.current_title()
    
    def _play_track(self, track):
        # print("Play: " + track)
        self.pipeline.set_state(Gst.State.READY)
        self.source.set_property('location', track)
        self.pipeline.set_state(Gst.State.PLAYING)
        
    def _set_volume(self, volume):
        if self.volctrl:
            self.volctrl.set_property('volume', volume/100.0)
            self.on_event(PLAYER_EVENT_VOLUME_CHANGED, volume)
