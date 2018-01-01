#!/usr/bin/env python3

import sys
import os
import argparse

from plugin_factory import PluginLoadError, PluginError

from events.control_events import *
from events.player_events import *
from events.app_events import *

from controllers import ControllerFactory
from players import PlayerFactory
from sources import SourceFactory, Playlist
from interfaces import EventOutFactory

if not os.environ.get("SPIRITBOX_PLUGIN_DIR"):
    PLUGINS_DIR = os.path.dirname(os.path.abspath(__file__))+"/plugins"
    os.environ["SPIRITBOX_PLUGIN_DIR"] = PLUGINS_DIR
else:
    PLUGINS_DIR = os.environ["SPIRITBOX_PLUGIN_DIR"]

sys.path.append(PLUGINS_DIR)

parser = argparse.ArgumentParser()

parser.add_argument('player', help='Select player')
parser.add_argument('controller', help='Select controller')
parser.add_argument('source', help='Select source. Example: dir=../Music')
parser.add_argument('-e', '--event_out', help='Event output', action='append')
parser.add_argument('-v', '--verbose', help='Print stuff', default=False)
args = parser.parse_args()

control = None
player = None
source = None
event_interfaces = []

verbose = False


def send_event(e):
    for evi in event_interfaces:
        evi.post_event(e)


def on_player_event(player_event):
    if verbose:
        print("Player event: " + str(player_event))

    send_event(player_event)

    if player_event == PLAYER_EVENT_TRACK_CHANGED:
        if verbose:
            print("Current track: " + str(player_event.data))
    elif player_event == PLAYER_EVENT_VOLUME_CHANGED:
        if verbose:
            print("Volume: " + str(player_event.data))


def on_control_event(event):
    if verbose:
        print("Received control event: " + event.name)

    send_event(event)

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
    elif event == CONTROL_EVENT_MUTE:
        player.mute()
    elif event == CONTROL_EVENT_UNMUTE:
        player.unmute()
    elif event == CONTROL_EVENT_MUTEUNMUTE:
        player.muted(not player.muted())
    elif event == CONTROL_EVENT_LIST:
        if verbose:
            for i, t in enumerate(player.playlist.list_titles()):
                if i == player.playlist.current_index():
                    print("==> " + str(i+1) + ":" + t)
                else:
                    print(str(i+1) + ":" + t)

        send_event(AppEvent(APP_EVENT_INDICATION,
                            AppIndication(APP_INDICATION_PLAYLIST,
                                          player.playlist.list_titles())))
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
    global event_interfaces
    global verbose

    verbose = args.verbose

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
        source_args = args.source.split("=")
        source_args.append("")
        source = pf.create(source_args[0], ''.join(source_args[1:]))
    except PluginLoadError as e:
        print(e)
        return 1
    except PluginError as e:
        print(e)
        return 1

    try:
        pf = EventOutFactory()
        if verbose:
            print("Event outputs: %s" % pf.get_available_types())
        for evo in args.event_out:
            eout_args = evo.split("=")
            eout_args.append("")
            eout = pf.create(eout_args[0], ''.join(eout_args[1:]))
            event_interfaces.append(eout)
    except PluginLoadError as e:
        print(e)
        return 1
    except PluginError as e:
        print(e)
        return 1

    player.playlist = Playlist(source)
    player.set_event_callback(on_player_event)

    send_event(AppEvent(APP_EVENT_INIT))
    send_event(AppEvent(APP_EVENT_READY))

    while 1:
        event = control.event()

        if event == CONTROL_EVENT_QUIT:
            break

        if event:
            on_control_event(event)

    send_event(AppEvent(APP_EVENT_SHUTDOWN))

    for e in event_interfaces:
        e.close()

    control.close()
    player.destroy()

    return 0


if __name__ == "__main__":
    sys.exit(main())
