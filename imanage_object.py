import json
import html
import requests
import re

from object_type import ObjectType

class IManageObject:
    def __init__(self, body):
        self._body = body
        if 'id' in body:
            self.id = body['id']
        else:
            self.id = 'None'
        if 'wstype' in body:
            self.wstype = ObjectType.value(body['wstype'])
        else:
            self.wstype = ObjectType.UNKNOWN
        if 'name' in body:
            self.id = body['name']
        else:
            self.id = '<empty>'
        self.session = None

    @property            
    def id(self): 
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property            
    def name(self): 
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property            
    def wstype(self): 
        return self._wstype

    @wstype.setter
    def wstype(self, value):
        self._wstype = value

    @property            
    def session(self): 
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property            
    def body(self): 
        return self._body

    @id.body
    def body(self, value):
        self._body = value

    def info(self):
        print('Object id: ' + self.id)
        print('Object type: ' + str(self.wstype))
        print('Session: ' + str(self.session))



