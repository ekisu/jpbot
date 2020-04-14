from abc import ABC, abstractmethod
from typing import List
from ..models.word import Word

class Source(object):
    @abstractmethod
    def search_for_word(self, word: str) -> List[Word]:
        pass
