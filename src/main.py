#!/usr/bin/env python3

import sys
import argparse
import traceback

from events.control_events import *
from events.player_events import *

from controllers import ControllerFactory
from players.gstplayer import GstPlayer
from sources import PlaylistFactory

parser = argparse.ArgumentParser()

parser.add_argument('controller', help='Select controller')
parser.add_argument('playlist', help='URI of input files') 

args = parser.parse_args()

control = None
player = None
playlist = None


def on_player_event(player_event):
    print("Player event: " + str(player_event))
    if player_event == PLAYER_EVENT_TRACK_CHANGED:
        print("Current track: " + str(player_event.data))
    elif player_event == PLAYER_EVENT_VOLUME_CHANGED:
        print("Volume: " + str(player_event.data))


def handle_control_event(event):
    print("Received control event: " + event.name)
    if event == CONTROL_EVENT_PLAY:
        player.play()
    elif event == CONTROL_EVENT_PAUSE:
        player.pause()
    elif event == CONTROL_EVENT_STOP:
        player.stop()
    elif event == CONTROL_EVENT_PLAYPAUSE:
        player.playing = not player.playing
    elif event == CONTROL_EVENT_NEXT:
        player.next_track()
    elif event == CONTROL_EVENT_PREV:
        player.prev_track()
    elif event == CONTROL_EVENT_VOL_UP:
        player.volume_up()
    elif event == CONTROL_EVENT_VOL_DOWN:
        player.volume_down()
    elif event == CONTROL_EVENT_LIST:
        for i, t in enumerate(player.playlist.list_titles()):
            if i == player.playlist.current_index():
                print("==> " + str(i+1) + ":" + t)
            else:
                print(str(i+1) + ":" + t)
    elif event == CONTROL_EVENT_JUMP:
        try:
            track_index = int(event.data)-1
        except:
            print("Invalid jump data")
            return
        if track_index >= 0:
            player.play_track(track_index)
    elif event == CONTROL_EVENT_MUTEUNMUTE:
        player.muted = not player.muted


def main():
    global player
    global control
    global playlist
    try:
        cf = ControllerFactory()
        print(cf.get_available_types())
        control = cf.create(args.controller)
    except:
        print("Cannot initialize controller")
        traceback.print_exc()
        return 1
    
    try:
        player = GstPlayer()
    except:
        print("Cannot initialize player")
        traceback.print_exc()
        return 1
    
    try:
        pf = PlaylistFactory()
        print(pf.get_available_types())
        playlist = pf.create(args.playlist)

    except:
        print("Cannot initialize playlist")
        traceback.print_exc()
        return 1
    
    print(str(playlist))
    
    player.playlist = playlist
    player.set_event_callback(on_player_event)
    
    while 1:
        event = control.event()

        if event == CONTROL_EVENT_QUIT:
            break

        if event:
            handle_control_event(event)
    
    player.destroy()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
