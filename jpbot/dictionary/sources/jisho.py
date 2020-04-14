from .common import Source
from typing import List
from ..models.word import Word, Reading, Sense
import requests

class JishoApiClient(object):
    API_BASE = "https://jisho.org/api/v1"
    def __init__(self):
        pass
    
    def search_by_word(self, word):
        endpoint = f"{self.API_BASE}/search/words"
        params = {
            "keyword": word
        }

        return requests.get(endpoint, params=params).json()

class JishoSource(Source):
    def __init__(self, api_client: JishoApiClient = JishoApiClient()):
        self.api_client: JishoApiClient = api_client

    def search_for_word(self, word: str) -> List[Word]:
        api_response = self.api_client.search_by_word(word)

        words = []
        for api_word in api_response["data"]:
            print(api_word["japanese"])
            readings = [Reading(r.get("word"), r.get("reading")) for r in api_word["japanese"]]
            senses = [Sense(s["english_definitions"]) for s in api_word["senses"]]

            words.append(Word(readings, senses))
        
        return words
