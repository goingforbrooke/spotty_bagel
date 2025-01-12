#!/usr/bin/env python3
"""
TODO: Add your module docstring here.
"""
from base64 import b64encode
from logging import basicConfig, DEBUG, debug, error, INFO, info, warning
from pathlib import Path
from subprocess import run as run_cli

from requests import get as http_get, post as http_post

"""Retrieve Spotify developer access token.

Get your token on [Spotify's developer site](https://developer.spotify.com/documentation/web-api) so you can use their web API.
- Create an application and get your `client_id` and `client_secret`
- 25-1-11 site doesn't open on Safari
    - Firefox works
"""
def get_spotify_access_token():
    # todo: Reuse Spotify access tokens (if they aren't expired yet) instead of getting a new one for each invocation.
    client_id, client_secret = get_client_id(), get_client_secret()

    token_url = "https://accounts.spotify.com/api/token"
    b64_id_secret = b64encode(f"{client_id}:{client_secret}".encode()).decode()
    request_headers = {"Content-Type": "application/x-www-form-urlencoded",
                       "Authorization": f"Basic {b64_id_secret}"}
    # &client_id={client_id}&client_secret={client_secret}
    request_data = {"grant_type": "client_credentials"}

    post_response = http_post(token_url, headers=request_headers, data=request_data)

    if post_response.status_code != 200:
        error_message = f"Non-200 response: {post_response.text}"
        error(error_message)
        raise RuntimeError(error_message)
    access_token = post_response.json()
    access_token = access_token["access_token"]

    debug(f"Retrieved a {len(access_token)} character access token (that's good for an hour)")
    return access_token


"""Search for a song on Spotify."""
def search_spotify_song(song_name, artist_name, limit_to):
    client_token = get_spotify_access_token()

    headers = {"Authorization": f"Bearer {client_token}"}
    song_query = f"track:{song_name}"
    if artist_name:
        song_query += f" artist:{artist_name}"
    request_url = f"https://api.spotify.com/v1/search?q={song_query}&type=track&limit={limit_to}"

    get_response = http_get(request_url, headers=headers)

    search_results = get_response.json()
    debug(f'Spotify found {search_results["tracks"]["total"]} tracks for "{song_name}" by {artist_name}')

    found_tracks = search_results['tracks']['items']
    return found_tracks


"""Get our client id.

Expects `client_id.txt` to be a sibling of `main.py`.
"""
def get_client_id():
    script_path = Path(__file__).resolve(strict=True)
    client_id = Path(script_path.parent, 'client_id.txt').read_text()
    return client_id


"""Get our client secret.

Expects `client_secret.txt` to be a sibling of `main.py`.
"""
def get_client_secret():
    # Get the path to `main.py`, not the symlink in `~/bin/`.
    script_path = Path(__file__).resolve(strict=True)
    client_secret = Path(script_path.parent, 'client_secret.txt').read_text()
    return client_secret


"""Get info about the song currently playing on BAGeL Radio."""
def get_bagel_song():
    bagel_stream_link = "http://ais-sa3.cdnstream1.com/2606_128.aac"
    headers = {
        "Icy-MetaData": "1"  # request ICY metadata
    }
    get_response = http_get(bagel_stream_link, headers=headers, stream=True)
    icy_metaint = int(get_response.headers['icy-metaint'])
    response_stream = get_response.raw
    # Skip initial stream data
    response_stream.read(icy_metaint)
    # Read metadata block (length byte * 16 bytes).
    metadata_length = ord(response_stream.read(1)) * 16
    if metadata_length > 0:
        found_metadata = response_stream.read(metadata_length).decode("utf-8", errors="ignore")
        # DEBUG:root:Found_metadata: StreamTitle='King Stingray - Day Off ';
        debug(f'Found_metadata: {found_metadata}')

        # Remove trailing null characters.
        trailing_nulls_removed = found_metadata.rstrip('\x00')
        # DEBUG:root:trailing_nulls_removed: StreamTitle='King Stingray - Day Off ';
        debug(f'trailing_nulls_removed: {trailing_nulls_removed}')

        # Remove trailing semicolon.
        trailing_semicolon_removed = trailing_nulls_removed.rstrip(';')
        # DEBUG:root:trailing_semicolon_removed: StreamTitle='King Stingray - Day Off '
        debug(f'trailing_semicolon_removed: {trailing_semicolon_removed}')

        metadata_key, song_info = trailing_semicolon_removed.split('=')
        assert (metadata_key == 'StreamTitle')
        # DEBUG:root:metadata_key: StreamTitle, song_info: 'King Stingray - Day Off '
        debug(f'metadata_key: {metadata_key}, song_info, {song_info}')

        # Remove squotes from song info.
        cleaned_info = song_info.lstrip("'").rstrip("'")
        # DEBUG:root:King Stingray - Day Off
        debug(f'cleaned_info: {cleaned_info}')

        # edge case: two en dashes like in "Yeah Yeah Yeahs - Y-Control"
        song_artist = cleaned_info.split('-')[0]
        song_title = cleaned_info.split('-')[1]

        # DEBUG:root:metadata_key, song_info: StreamTitle, 'King Stingray - Day Off '
        debug(f'song_artist: {song_artist}, song_title: {song_title}')

        cleaned_artist, cleaned_title = song_artist.strip(), song_title.strip()
        debug(f'cleaned_artist: {cleaned_artist}, cleaned_title: {cleaned_title}')

        found_song = {'artist': cleaned_artist, 'title': cleaned_title}
        info(f'🥯 Current BAGeL song: {found_song}')
        return found_song


"""Open a song in Spotify (and it'll start playing).

# Example

`open -a Spotify https://open.spotify.com/track/5J8NNFnkQI2YjUcE0o2PLT`
"""
def open_in_spotify_app(track_url):
    assert track_url.startswith('https://open.spotify.com/')
    cli_cmd = ['open', '-a', 'Spotify', track_url]
    run_cli(cli_cmd)

    debug('Opened track in Spotify app')
    return True


def main():
    # Show all log messages.
    basicConfig(level=INFO)

    current_song = get_bagel_song()

    # Search Spotify for the song.
    found_tracks = search_spotify_song(current_song['title'], artist_name=current_song['artist'], limit_to=5)

    # Reduce track information to what we're interested in so search results take up less terminal height in the next space.
    # found_track.keys(): dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'is_playable', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
    winnowed_tracks = [{'track_name': found_track['name'],
                        'artist_name': [artist['name'] for artist in found_track['artists']],
                        'album_name': found_track['album']['name'],
                        'track_popularity': found_track['popularity'],
                        'song_link': found_track['external_urls']['spotify']}
                       for found_track in found_tracks]
    # Display simplified search results in the terminal
    from pprint import pprint; pprint(winnowed_tracks)

    if len(winnowed_tracks) > 0:
        # Open first result in Spotify (and start playing it).
        first_result = winnowed_tracks[0]['song_link']
        open_in_spotify_app(first_result)
    else:
        warning_message = '😱 No songs were found, so we\'re exiting early without opening the first result in Spotify.'
        warning(warning_message)
        exit(0)

    info("✅ Done")


if __name__ == "__main__":
    main()
