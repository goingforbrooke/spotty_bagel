"""BAGeL Radio-related operations."""
from logging import debug, info

from requests import get as http_get


"""Get info about the song currently playing on BAGeL Radio.

We don't require that BAGeL Radio to be playing through VLC Media Player for this to work.
"""
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
