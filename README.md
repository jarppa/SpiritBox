# SpiritBox
SpiritBox is a super simple modular audio player written in Python.

## Modules
SpiritBox can be fully customized with modules.

### Control
Control modules are responsible of controlling the playback.

### Source
Source modules control provide access to the audio files.

### Player
Player module provides implementation of the audio player.

## Shipped modules
SpiritBox ships with some basic modules.

### console (control)
CLI based control.

### keyboard (control)
Standard keyboard control with multimedia keys.

### dir (Source)
Audio file source from a directory. (MP3 only)

### gst (Player)
GStreamer audio player.

# Example usage:
 $ python3 main.py gst console dir=[path_to_audio_files]
