# Copyright (c) 2022. K2-Software
# All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.

import json
import html
import os
import requests
import re
import tempfile

from imanage_object import IManageObject

class IManageDocument(IManageObject):
    def __init__(self, body):
        super().__init__(body)
        self._data = None

    def get_filename(self):
        if 'name' in self.body and 'extension' in self.body:
            return self.body['name'] + '.' + self.body['extension']
        elif 'name' in self.body:
            return self.body['name']
        else:
            return next(tempfile._get_candidate_names())
        
    def persist(self, path):
        if self._data is None:
            self.session.get_imanage_document(self)
        if self._data is None:
            return False
        with open(os.path.join(path, self.get_filename()), "wb") as target_file:
            target_file.write(self._data)
        return True
