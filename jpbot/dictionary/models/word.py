from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Reading(object):
    word: Optional[str]
    reading: Optional[str]

@dataclass
class Sense(object):
    definitions: List[str]

@dataclass
class Word(object):
    readings: List[Reading]
    senses: List[Sense]
