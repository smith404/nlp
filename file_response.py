import json

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

class FileResponse:
    def __init__(self, filename):
        self._filename = filename
        self._original_filename = filename

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @property            
    def original_filename(self): 
        return self._original_filename

    @original_filename.setter
    def original_filename(self, value):
        self._original_filename = value

    @original_filename.deleter
    def original_filename(self):
        del self._original_filename

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

    def is_pdf(self):
        return self.get_extnesion(self) == 'pdf'

    def is_text(self):
        return self.get_extnesion(self) == 'txt'
