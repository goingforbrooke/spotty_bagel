#!/usr/bin/env python3
"""
TODO: Add your module docstring here.
"""
from pathlib import Path
from logging import error, info, warning
from base64 import b64encode

from requests import get as http_get, post as http_post

"""Retrieve Spotify developer access token.

Get your token on [Spotify's developer site](https://developer.spotify.com/documentation/web-api) so you can use their web API.
- Create an application and get your `client_id` and `client_secret`
- 25-1-11 site doesn't open on Safari
    - Firefox works
"""
def get_spotify_access_token():
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

    info(f"Got {len(access_token)} character access token")
    return access_token


"""Search for a song on Spotify."""
def search_spotify_song(song_name, artist_name=None):
    client_token = get_spotify_access_token()

    headers = {"Authorization": f"Bearer {client_token}"}
    song_query = f"track:{song_name}"
    if artist_name:
        song_query += f" artist:{artist_name}"
    request_url = f"https://api.spotify.com/v1/search?q={song_query}&type=track"

    get_response = http_get(request_url, headers=headers)

    info("Searched for song on Spotify")
    return get_response.json()


"""Get our client id."""
def get_client_id():
    client_id = Path('client_id.txt').read_text()
    return client_id


"""Get our client secret."""
def get_client_secret():
    client_secret = Path('client_secret.txt').read_text()
    return client_secret


def main():
    info("Done")


if __name__ == "__main__":
    main()
