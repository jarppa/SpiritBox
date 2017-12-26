#!/usr/bin/env python3

import sys
import os
import argparse

from plugin_factory import PluginLoadError, PluginError

from events.control_events import *
from events.player_events import *

from controllers import ControllerFactory
from players import PlayerFactory
from sources import SourceFactory, Playlist

if not os.environ.get("SPIRITBOX_PLUGIN_DIR"):
    PLUGINS_DIR = os.path.dirname(os.path.abspath(__file__))+"/plugins"
    os.environ["SPIRITBOX_PLUGIN_DIR"] = PLUGINS_DIR
else:
    PLUGINS_DIR = os.environ["SPIRITBOX_PLUGIN_DIR"]

sys.path.append(PLUGINS_DIR)

parser = argparse.ArgumentParser()

parser.add_argument('player', help='Select player')
parser.add_argument('controller', help='Select controller')
parser.add_argument('playlist', help='URI of input files') 
parser.add_argument('--verbose', help='Print stuff', default=False)
args = parser.parse_args()

control = None
player = None
source = None
verbose = False


def on_player_event(player_event):
    if verbose:
        print("Player event: " + str(player_event))
    if player_event == PLAYER_EVENT_TRACK_CHANGED:
        print("Current track: " + str(player_event.data))
    elif player_event == PLAYER_EVENT_VOLUME_CHANGED:
        print("Volume: " + str(player_event.data))


def handle_control_event(event):
    if verbose:
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
    global source

    if verbose:
        print(PLUGINS_DIR)

    try:
        cf = ControllerFactory()
        if verbose:
            print("Controllers: %s" % cf.get_available_types())
        controller_args = args.controller.split("=")
        controller_args.append("")
        control = cf.create(controller_args[0], ''.join(controller_args[1:]))
    except PluginLoadError as e:
        print(e)
        return 1
    except PluginError as e:
        print(e)
        return 1

    try:
        pf = PlayerFactory()
        if verbose:
            print("Players: %s" % pf.get_available_types())
        player_args = args.player.split("=")
        player_args.append("")
        player = pf.create(player_args[0], ''.join(player_args[1:]))
    except PluginLoadError as e:
        print(e)
        return 1
    except PluginError as e:
        print(e)
        return 1

    try:
        pf = SourceFactory()
        if verbose:
            print("Sources: %s" % pf.get_available_types())
        source_args = args.playlist.split("=")
        source_args.append("")
        source = pf.create(source_args[0], ''.join(source_args[1:]))
    except PluginLoadError as e:
        print(e)
        return 1
    except PluginError as e:
        print(e)
        return 1

    player.playlist = Playlist(source)
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
