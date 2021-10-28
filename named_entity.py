import json

class NamedEntity:
    def __init__(self, ent, kind, start, end):
        self.ent = ent
        self.kind = kind
        self.start = start
        self.end = end

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
