from .common import Source
from ..models.song import Song, SongLyric
import requests
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import quote

class MusixmatchSource(Source):
    BASE_URL = 'https://www.musixmatch.com'
    SEARCH_URL = '/pt-br/search/'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }

    def _parse_lyrics_page(self, contents: str) -> Optional[str]:
        lyrics_soup = BeautifulSoup(contents, 'html.parser')
        lyric_elements = lyrics_soup.findAll('p', class_='mxm-lyrics__content')
        if len(lyric_elements) == 0:
            return None

        return '\n'.join(lyric_element.text for lyric_element in lyric_elements)

    def _search_term(self, term: str) -> Optional[str]:
        response = requests.get(self.BASE_URL + self.SEARCH_URL + quote(term), headers=self.HEADERS)

        soup = BeautifulSoup(response.text, 'html.parser')
        card_title = soup.find(class_='media-card-title')

        if card_title is None:
            return None

        link = card_title.find('a')['href']
        lyrics_response = requests.get(self.BASE_URL + link, headers=self.HEADERS)
        return self._parse_lyrics_page(lyrics_response.text)

    def search_for_artist_and_title(self, artist: str, title: str) -> Optional[Song]:
        # Don't actually use the artist because Musixmatch seems to have a brain death???
        search_term = f"{title}"
        lyrics = self._search_term(search_term)

        if lyrics is None:
            return None

        song_lyric = SongLyric(
            lyrics = lyrics
        )
        
        return Song(artist, title, song_lyric)
