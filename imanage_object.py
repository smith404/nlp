# Copyright (c) 2022. K2-Software
# All software, both binary and source published by K2-Software (hereafter, Software) is copyrighted by the author (hereafter, K2-Software) and ownership of all right, title and interest in and to the Software remains with K2-Software. By using or copying the Software, User agrees to abide by the terms of this Agreement.

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
        if 'database' in body:
            self.database = body['database']
        else:
            self.database = 'None'
        if 'wstype' in body:
            self.wstype = ObjectType.value(body['wstype'])
        else:
            self.wstype = ObjectType.UNKNOWN
        if 'name' in body:
            self.name = body['name']
        else:
            self.name = '<empty>'

        self.session = None

    @property            
    def id(self): 
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property            
    def database(self): 
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

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

    @body.setter
    def body(self, value):
        self._body = value

    def info(self):
        print(self.database + '!' + str(self.wstype) + ': ' + self.name + ' (' + self.id + ')')
        if self.session is None:
            print('No session found')



