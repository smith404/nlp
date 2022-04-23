import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageLibrary(IManageObject):
    def __init__(self, body):
        super().__init__(body)
