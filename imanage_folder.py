import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageFolder(IManageObject):
    def __init__(self, folder_id):
        super().__init__(folder_id)

    def info(self):
        print('Folder id: ' + self.id)