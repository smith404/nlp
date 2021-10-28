import json

class PartOfSpeech:
    def __init__(self, text, lemma, pos, tag, dep, shape, alpha, stop):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.tag = tag
        self.dep = dep
        self.shape = shape
        self.alpha = alpha
        self.stop = stop

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
