"""Spotify-related operations."""
from base64 import b64encode
from logging import error, debug
from pathlib import Path
from subprocess import run as run_cli

from requests import post as http_post, get as http_get

from utils import application_is_installed


"""Open a song in Spotify (and it'll start playing).

# Example

`open -a Spotify https://open.spotify.com/track/5J8NNFnkQI2YjUcE0o2PLT`
"""
def open_in_spotify_app(track_url):
    # todo: Add an option to open song in Spotify webapp instead of app.
    application_is_installed('open', throw_error=True)
    application_is_installed('Spotify', throw_error=True)

    assert track_url.startswith('https://open.spotify.com/')

    cli_cmd = ['open', '-a', 'Spotify', track_url]
    # Error out on non-zero return codes.
    run_cli(cli_cmd, check=True)

    debug('Opened track in Spotify app')
    return True


"""Search for a song on Spotify.

Uses Spotify's [search API](https://developer.spotify.com/documentation/web-api/reference/search)
"""
def search_spotify_song(song_name, artist_name, limit_to) -> list:
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


