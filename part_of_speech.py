import json

class PartOfSpeech:
    def __init__(self, text, ent_type, lemma, pos, tag, dep, shape, alpha, stop):
        self.text = text.strip().replace("\n", " ")
        self.ent_type = ent_type
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
