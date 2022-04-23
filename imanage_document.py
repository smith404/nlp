# Copyright (c) 2022. K2-Software
# All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.

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
        
