#!/usr/bin/env python3
"""
TODO: Add your module docstring here.
"""
from requests import get as http_get, post as http_post

"""Retrieve Spotify developer access token.

Get your token on [Spotify's developer site](https://developer.spotify.com/documentation/web-api) so you can use their web API.
- Create an application and get your `client_id` and `client_secret`
- 25-1-11 site doesn't open on Safari
"""
def get_spotify_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    headers = {"Authorization": f"Basic {client_id}:{client_secret}"}
    response = http_post(url, headers=headers, data=data)
    return response.json()["access_token"]


"""Search for a song on Spotify."""
def search_spotify_song(song_name, artist_name=None):
    token = get_spotify_access_token("your_client_id", "your_client_secret")
    headers = {"Authorization": f"Bearer {token}"}
    query = f"track:{song_name}"
    if artist_name:
        query += f" artist:{artist_name}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    response = http_get(url, headers=headers)
    return response.json()

def main():
    print("Done")


if __name__ == "__main__":
    main()
