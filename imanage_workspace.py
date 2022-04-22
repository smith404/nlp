import json
import html
import requests
import re

from imanage_object import IManageObject

class IManageWorkspace(IManageObject):
    def __init__(self, body):
        super().__init__(body)

