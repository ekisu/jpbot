from .common import Source
from ..models.song import Song, SongLyric
from typing import Optional
from lyricsgenius import Genius

class GeniusSource(Source):
    def __init__(self, genius_api_client: Genius):
        self.genius: Genius = genius_api_client
    
    def search_for_artist_and_title(self, artist: str, title: str) -> Optional[Song]:
        result = self.genius.search_song(title, artist, get_full_info=False)

        if result is None:
            return None
        
        lyric = SongLyric(
            lyrics = result.lyrics
        )

        song = Song(artist, title, lyric)
        return song
        