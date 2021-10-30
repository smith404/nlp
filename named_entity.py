import json

class NamedEntity:
    def __init__(self, text, ent_type, start, end):
        self.text = text.strip().replace("\n", "")
        self.ent_type = ent_type
        self.start = start
        self.end = end

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
