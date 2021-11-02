import json

class Span:
    def __init__(self, text, label, start, end, sentiment):
        self.text = text.strip().replace("\n", " ")
        self.label = label
        self.start = start
        self.end = end
        self.sentiment = sentiment

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
