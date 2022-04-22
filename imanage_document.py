import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageDocument(IManageObject):
    def __init__(self, folder_id):
        super().__init__(folder_id)

    def info(self):
        print('Document id: ' + self.id)