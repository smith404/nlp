import json
import html
import traceback
import requests
import re

from requests.packages.urllib3.exceptions import InsecureRequestWarning

# We are ignoring certificate warnings so we don't want wanrnings all the time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class IManageSession:
    def __init__(self, baseURL, token):
        self._baseURL = baseURL
        self._token = token
        self._state = 200

    @property            
    def state(self): 
        return self._state

    @state.setter
    def token(self, value):
        self._state = value

    @property            
    def token(self): 
        return self._state

    @token.setter
    def token(self, value):
        self._token = value

    @property            
    def baseURL(self): 
        return self._baseURL

    @baseURL.setter
    def baseURL(self, value):
        self._baseURL = value

    def make_header(self):
        return { 'Authorization' : 'Bearer ' + self.token }

    def get_imamage_data(self, url_path):
        url = self.baseURL + url_path
        try:
            response = requests.get(url, headers=self.make_header(), verify=False)
            self.state = response.status_code
            if response.status_code == 200:
                return response.json()
        except:
            traceback.print_exc()
            self.state = 500
        return {}

    def get_imamage_document(self, doc_id):
        text = {}
        text['body'] = ''
        url = self.baseURL + 'documents/' + doc_id + '/download'
        try:
            response = requests.get(url, headers=self.make_header(), verify=False)
            self.state = response.status_code
            if response.status_code == 200:
                text['body'] = response.text
        except:
            traceback.print_exc()
            self.state = 500
        return json.dumps(text)        