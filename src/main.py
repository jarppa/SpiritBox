#!/usr/bin/env python3

import sys
import argparse
import traceback

parser = argparse.ArgumentParser()

parser.add_argument('controller', help='Select controller [Keyboard | Remote | none]')
parser.add_argument('--output', help='Audio output device')
parser.add_argument('playlist', help='URI of input files') 

args = parser.parse_args()

from controllers import ControllerFactory
from players.gstplayer import GstPlayer
from sources import PlaylistFactory
from players import PLAYER_EVENT_STARTED, \
                PLAYER_EVENT_STOPPED, \
                PLAYER_EVENT_PAUSED, \
                PLAYER_EVENT_VOLUME_CHANGED, \
                PLAYER_EVENT_TRACK_CHANGED, \
                PLAYER_EVENT_TRACK_INFO, \
                PLAYER_EVENT_ERROR
control = None
player = None
playlist = None
    
def on_player_event(player_event):
    print("Player event: "+ str(player_event))
    if player_event == PLAYER_EVENT_STARTED:
        print("Current track: "+player.get_current_track())

def handle_event(event):
    print ("Received event: " +event)
    if event == "EVENT_PLAY":
        player.play()
    elif event == "EVENT_STOP":
        player.stop()
    elif event == "EVENT_PAUSE":
        player.pause()
    elif event == "EVENT_NEXT":
        player.next_track()
    elif event == "EVENT_PREV":
        player.prev_track()
    elif event == "EVENT_VOL_UP":
        player.volume_up()
    elif event == "EVENT_VOL_DOWN":
        player.volume_down()

def main():
    global player
    global control
    global playlist
    try:
        cf = ControllerFactory()
        print (cf.get_available_types())
        control = cf.create(args.controller)
    except:
        print ("Cannot initialize controller")
        traceback.print_exc()
        return 1
    
    try:
        player = GstPlayer(args.output)
    except:
        print ("Cannot initialize player")
        traceback.print_exc()
        return 1
    
    try:
        pf = PlaylistFactory()
        print (pf.get_available_types())
        playlist = pf.create(args.playlist)

    except:
        print ("Cannot initialize playlist")
        traceback.print_exc()
        return 1
    
    print (str(playlist))
    
    player.set_playlist(playlist)
    player.set_event_callback(on_player_event)
    
    while(1):
        event = control.get_event()
        
        if not event or event == "EVENT_QUIT":
            break
        
        handle_event(event)
    
    player.destroy()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
