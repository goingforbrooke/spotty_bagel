# Spotty Bagel

Open the song playing on [BAGeL Radio](https://www.bagelradio.com) in Spotify.

# Requirements

- MacOS
- Python
- python requests

# Installation

1. Add `main.py` to `PATH`.

Ensure that `~/bin` exists.

```console
mkdir -p ~/bin
```

Ensure that `~/bin`'s on your `PATH`.

```console
echo $PATH | grep bin
```

Create a symbolic link to `spotty_bagel/main.py` in `~/bin`.

```console
ln -s spotty_bagel/main.py ~/bin/main.py
```

Or use my application [Binify](https://github.com/goingforbrooke/binify) to do it for you.

2. Get a developer client ID and secret for Spotify with [these instructions](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
 
3. (Optional) Add [BAGeL Radio](https://www.bagelradio.com) to [VLC Media Player](https://www.bagelradio.com) with 

# Usage

Run `spotty_bagel` in your terminal when there's a song on that you like and it'll open (and start playing) in Spotify.
