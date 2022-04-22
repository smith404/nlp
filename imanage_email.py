import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageEmail(IManageObject):
    def __init__(self, body):
        super().__init__(body)

