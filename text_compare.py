import json
import re

class TextCompare:
    def __init__(self, first, second):
        self._first_text = first
        self._second_text = second
        self._score = True

    @property            
    def score(self): 
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @score.deleter
    def score(self):
        del self._score


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
