from dataclasses import dataclass
from typing import Optional

@dataclass
class SongLyric(object):
    lyrics: Optional[str]

@dataclass
class Song(object):
    artist: str
    title: str
    lyrics: SongLyric
