import json

class FileResponse:
    def __init__(self, filename):
        self._filename = filename

    @property            
    def filename(self): 
        return self._filename
    #
    @filename.setter
    def filename(self, value):
        self._filename = value

    @filename.deleter
    def filename(self):
        del self._filename

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_extnesion(self):
        if '.' in self.filename:
            return self.filename.rsplit('.', 1)[1].lower()
        return ""
