from abc import ABC, abstractmethod
from typing import Optional
from ..models.song import Song

class Source(object):
    @abstractmethod
    def search_for_artist_and_title(self, artist: str, title: str) -> Optional[Song]:
        pass
