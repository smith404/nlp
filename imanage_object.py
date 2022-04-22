from asyncio.windows_events import NULL
import json
import html
import requests
import re

class IManageObject:
    def __init__(self, id):
        self._id = id
        self._session = NULL

    @property            
    def id(self): 
        return self._id

    @id.setter
    def token(self, value):
        self._id = value

    @property            
    def session(self): 
        return self._session

    @id.setter
    def session(self, value):
        self._session = value
