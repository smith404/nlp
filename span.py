import json

class Span:
    # Running number to ensure all spans have a unique id
    _id = 0

    def __init__(self, text, label, start, end):
        self.text = text.strip().replace("\n", " ")
        self.label = label
        self.start = start
        self.end = end
        __class__._id = __class__._id + 1
        self.id = __class__._id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
