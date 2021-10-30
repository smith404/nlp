import json
import fitz

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

class FileResponse:
    def __init__(self, filename):
        self._filename = filename
        self._original_filename = filename
        self._sucess = True

    @staticmethod
    def text_from_pdf(filename):
        content = ''
        doc = fitz.open(filename)
        for page in doc:
            content = content + page.get_text('text')
            content = content + " "

        return content

    @staticmethod
    def text_from_docx(filename):
        return ''

    @property            
    def sucess(self): 
        return self._sucess

    @sucess.setter
    def sucess(self, value):
        self._sucess = value

    @sucess.deleter
    def sucess(self):
        del self._sucess

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
    
    @filename.setter
    def filename(self, value):
        self._filename = value

    @filename.deleter
    def filename(self):
        del self._filename

    def allowed_file(self):
        return '.' in self._original_filename and \
        self._original_filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_extnesion(self):
        if '.' in self.original_filename:
            return self.original_filename.rsplit('.', 1)[1].lower()
        return "tmp"

    def is_pdf(self):
        return self.get_extnesion(self) == 'pdf'

    def is_text(self):
        return self.get_extnesion(self) == 'txt'
