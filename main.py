#!/usr/bin/env python3
"""
TODO: Add your module docstring here.
"""
from logging import basicConfig, DEBUG, info, warning

from bagel import get_bagel_song
from display import calculate_widest_cell, display_table_headers, display_search_results, winnow_tracks
from spotify import open_in_spotify_app, search_spotify_song
from vlc import toggle_vlc_playback


def main():
    # Show all log messages.
    basicConfig(level=DEBUG)

    # Get info about the current song playing on BAGeL radio.
    current_song = get_bagel_song()

    # Search Spotify for the top five matches.
    found_tracks = search_spotify_song(current_song['title'], artist_name=current_song['artist'], limit_to=5)

    # Reduce track info to the fields that we're interested in displaying.
    winnowed_tracks = winnow_tracks(found_tracks)

    # Display search results in the terminal.
    widest_cell = calculate_widest_cell(winnowed_tracks)
    display_table_headers(widest_cell, winnowed_tracks)
    display_search_results(widest_cell, winnowed_tracks)

    # Pause VLC so the audio doesn't overlap.
    # todo: Add a `spotty_bagel` CLI flag that disables pausing in VLC.
    toggle_vlc_playback()

    # Open the first search result in Spotify.
    if len(winnowed_tracks) > 0:
        # Open first result in Spotify (and start playing it).
        first_result = winnowed_tracks[0]['song_link']
        # todo: Add a `spotty_bagel` CLI flag that disables opening in Spotify.
        open_in_spotify_app(first_result)
    # Otherwise, exit early if there is no track to open.
    else:
        warning_message = '😱 No songs were found, so we\'re exiting early without opening the first result in Spotify.'
        warning(warning_message)
        exit(0)

    info("✅ Done")


if __name__ == "__main__":
    main()
