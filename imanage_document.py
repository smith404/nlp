import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageDocument(IManageObject):
    def __init__(self, body):
        super().__init__(body)

    def get_filename(self):
        if 'name' in self.body and 'extension' in self.body:
            return self.body['name'] + '.' + self.body['extension']
        elif 'name' in self.body:
            return self.body['name']
        else:
            return 'unknown-file-name'
        
