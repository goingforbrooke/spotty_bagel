"""VLC-related operations."""
from logging import error, info
from platform import system
from subprocess import run as run_cli

from utils import application_is_installed

"""Pause or play VLC media player (which plays BAGeL Radio) on MacOS.

# Setup

[Add BAGeL Radio to VLC](https://wiki.videolan.org/VLC_HowTo/Listen_to_online_radio/).

# How it Works

There's no "pause" command, but sending "play" while something's already playing has the same effect.

```console
osascript -e 'tell application "VLC" to play'
```
"""
def toggle_vlc_playback():
    # Don't throw an error if VLC's not installed b/c we want to show the download link.
    if not application_is_installed('VLC', throw_error=False):
        error_message = f"VLC Media player isn't installed. Get it here: http://www.videolan.org"
        error(error_message)
        raise RuntimeError(error_message)
    # todo: Make vlc playback toggle platform-independent (and not just MacOS).
    host_platform = system()
    if host_platform != 'Darwin':
        error_message = f'Toggling VLC not available on {host_platform}'
        error(error_message)
        # todo: Add VLC toggle support for non-MacOS platforms.
        raise NotImplemented(error_message)

    cli_args = ('osascript', '-e', 'tell application "VLC" to play')
    # Error out on non-zero return codes.
    run_cli(cli_args, True)

    info('⏯️ Paused or resumed playback of VLC media player.')
    return True
