"""Terminal-display related operations."""
from logging import debug


"""Calculate the width of the widest cell that we're going to display in the terminal."""
def calculate_widest_cell(winnowed_tracks):
    headers_and_cells = []
    # Use the widest cell as the column width.
    for winnowed_track in winnowed_tracks:
        for row_header, row_cell in winnowed_track.items():
            headers_and_cells.append(str(row_header))
            # Don't let hyperlinks throw off table formatting.
            if not str(row_cell).startswith('http'):
                headers_and_cells.append(str(row_cell))
    widest_cell = max(len(header_or_cell) for header_or_cell in headers_and_cells)
    debug(f'Widest cell is {widest_cell} characters wide')
    return widest_cell


"""Show headers for the search results table in the terminal."""
def display_table_headers(column_width, winnowed_tracks):
    assert len(winnowed_tracks) > 0
    # Get the first track b/c doesn't matter which track we get, since they all have the same headers.
    first_track = winnowed_tracks[0]
    # Display table headers.
    spaced_headers = (raw_header.replace('_', ' ') for raw_header in first_track.keys())
    pretty_headers = (spaced_header.title() for spaced_header in spaced_headers)
    table_headers = [f"{str(table_header):<{column_width}}" for table_header in pretty_headers]
    display_headers = ' '.join(table_headers)
    print(display_headers)
    print('-' * sum(len(str(table_header)) for table_header in table_headers))


"""Show search results in the terminal."""

def display_search_results(column_width, winnowed_tracks):
    # Display simplified search results in the terminal
    for winnowed_track in winnowed_tracks:
        display_tidbits = [f"{str(value):<{column_width}}" for value in winnowed_track.values()]
        display_row = ' '.join(display_tidbits)
        print(display_row)


"""Reduce track information to what we're interested in so search results take up less terminal height in the next space.

# Known Keys in Found Tracks

- **album**
- **artists**
- available_markets
- disc_number
- duration_ms
- explicit
- external_ids
- **external_urls**
- href
- id
- is_local
- is_playable
- **name**
- **popularity**
- preview_url
- track_number
- type
- uri
"""


def winnow_tracks(found_tracks):
    winnowed_tracks = [{'track_name': found_track['name'],
                        # Assume one artist.
                        'artist_name': [artist['name'] for artist in found_track['artists']][0],
                        'album_name': found_track['album']['name'],
                        'track_popularity': found_track['popularity'],
                        'song_link': found_track['external_urls']['spotify'], }
                       for found_track in found_tracks]
    return winnowed_tracks
