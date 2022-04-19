import json
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

class TextResponse:
    def __init__(self, text):
        self._original_text = text
        self._normal_text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text.lower()) 
        self._sucess = True
        nltk.download('stopwords')

    @staticmethod
    def remove_punctuation(text):
        final = " ".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
        return final

    @property            
    def sucess(self): 
        return self._sucess

    @sucess.setter
    def sucess(self, value):
        self._sucess = value

    @sucess.deleter
    def sucess(self):
        del self._sucess

    def remove_stop_words(self):
        stop = stopwords.words('english')
        return " ".join([word for word in self._normal_text.split() if word not in (stop)])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
